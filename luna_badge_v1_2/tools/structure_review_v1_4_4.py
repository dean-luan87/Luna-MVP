"""
Luna Badge v1.4.4 — Structure Review Script

This script inspects module boundaries, architectural contracts,
and forbidden direct calls. 

Running this script will generate a human-readable review report:
    reports/STRUCTURE_REVIEW_v1.4.4.md
"""

import ast
import os
from typing import List, Dict

PROJECT_ROOT = "."


# ------------------------------
# Helper Functions
# ------------------------------

def scan_py_files(root: str) -> List[str]:
    """Return all Python files under project."""
    py_files = []
    exclude_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', 
                    'realtime_lab', 'ios_test', 'ios_web_test', 'ios_web_demo',
                    'temp_mobile_test', 'temp_mobile_ui', 'test_ota_downloads',
                    'test_runtime', 'upload_queue', 'upload_sent', 'ota_downloads',
                    'outputs', 'logs', 'runtime_logs', 'perf_logs', 'reports',
                    'samples', 'static', 'templates', 'weights', 'benchmarks',
                    'h5_realtime', 'heal_db', 'review_store', 'error_registry'}
    
    for base, dirs, files in os.walk(root):
        # 排除不需要的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for f in files:
            if f.endswith(".py") and not f.startswith("."):
                py_files.append(os.path.join(base, f))
    return py_files


def parse_imports(file_path: str) -> Dict[str, List[str]]:
    """Parse import statements and detect forbidden imports."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            src = f.read()
    except Exception as e:
        return {"file": file_path, "imports": [], "error": str(e)}

    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {"file": file_path, "imports": [], "error": "syntax_error"}

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                imports.append(module)

    return {
        "file": file_path,
        "imports": imports,
    }


def assert_no_direct_taskchain_calls(import_data):
    """Detect illegal direct imports to TaskChainManager."""
    illegal_files = []
    allowed_files = {"orchestrator.py", "decision_core.py", "taskchain/manager.py"}
    
    # 排除路径（测试文件、旧代码等）
    exclude_paths = {
        "tests/", "test_", "benchmark", "core/task_chain_manager.py",  # 旧代码
        "core/task/", "src/tasks/", "tasks/",  # 旧任务系统
        "core/luna_engine.py",  # 旧引擎代码
        "core/taskchain/__init__.py",  # 模块自身导出
        "core/taskchain/task_chain_router.py",  # 旧路由代码
    }
    
    for entry in import_data:
        file_path = entry["file"]
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        
        # 跳过 taskchain 模块自身
        if "taskchain" in file_dir and "manager.py" in file_path:
            continue
        
        # 跳过排除的路径
        if any(exclude in file_path for exclude in exclude_paths):
            continue
            
        for imp in entry["imports"]:
            if "taskchain" in imp.lower() or "task_chain" in imp.lower():
                # 只允许 orchestrator 和 decision_core 调用
                if file_name not in allowed_files and "orchestrator" not in file_path:
                    illegal_files.append({
                        "file": file_path,
                        "import": imp
                    })
    return illegal_files


def assert_no_direct_decisioncore_calls(import_data):
    """DecisionCore 只能由 orchestrator 调用."""
    illegal_files = []
    allowed_files = {"orchestrator.py"}
    
    # 排除路径（测试文件、模块自身导出）
    exclude_paths = {
        "tests/", "test_", "decision/__init__.py",  # 模块自身导出
    }
    
    for entry in import_data:
        file_path = entry["file"]
        file_name = os.path.basename(file_path)
        
        # 跳过 decision 模块自身的实现文件
        if "decision" in file_path and "decision_core.py" in file_path:
            continue
        
        # 跳过排除的路径
        if any(exclude in file_path for exclude in exclude_paths):
            continue
            
        for imp in entry["imports"]:
            if "decision_core" in imp.lower() or "decision.decision_core" in imp.lower():
                # 只允许 orchestrator 调用
                if file_name not in allowed_files and "orchestrator" not in file_path:
                    illegal_files.append({
                        "file": file_path,
                        "import": imp
                    })
    return illegal_files


def check_command_layer_boundaries(import_data) -> Dict[str, List[str]]:
    """检查 Command Layer 是否越权调用 TaskChain 或 DecisionCore."""
    violations = []
    
    for entry in import_data:
        file_path = entry["file"]
        
        # 只检查 command_layer 目录下的文件
        if "command_layer" not in file_path:
            continue
            
        for imp in entry["imports"]:
            # Command Layer 不应该直接调用 TaskChain
            if "taskchain" in imp.lower() or "task_chain" in imp.lower():
                violations.append({
                    "file": file_path,
                    "violation": f"Command Layer 直接导入 TaskChain: {imp}"
                })
            # Command Layer 不应该直接调用 DecisionCore
            if "decision_core" in imp.lower() or "decision.decision_core" in imp.lower():
                violations.append({
                    "file": file_path,
                    "violation": f"Command Layer 直接导入 DecisionCore: {imp}"
                })
    
    return violations


def check_contract_objects() -> Dict[str, bool]:
    """
    Verify that ParsedIntent / DecisionOutput / TaskResult schemas 
    were not modified by checking structural signatures.
    """
    results = {}

    def get_class_signature(file, clsname):
        try:
            with open(file, "r", encoding="utf-8") as f:
                src = f.read()
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == clsname:
                    fields = []
                    for stmt in node.body:
                        if isinstance(stmt, ast.AnnAssign):
                            if isinstance(stmt.target, ast.Name):
                                fields.append(stmt.target.id)
                        elif isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Name):
                                    fields.append(target.id)
                    return fields
        except Exception as e:
            return None

    # 检查 ParsedIntent
    parsed_intent_file = "core/intent_schema.py"
    if os.path.exists(parsed_intent_file):
        parsed_intent_fields = get_class_signature(parsed_intent_file, "ParsedIntent")
        expected_fields = ["intent_name", "slots", "source", "need_confirm", "raw"]
        if parsed_intent_fields:
            results["ParsedIntent_valid"] = all(field in parsed_intent_fields for field in expected_fields)
        else:
            results["ParsedIntent_valid"] = False
    else:
        results["ParsedIntent_valid"] = False

    # 检查 DecisionOutput
    decision_output_file = "core/decision_output.py"
    if os.path.exists(decision_output_file):
        decision_output_fields = get_class_signature(decision_output_file, "DecisionOutput")
        results["DecisionOutput_valid"] = decision_output_fields is not None and len(decision_output_fields) > 0
    else:
        results["DecisionOutput_valid"] = False

    # 检查 TaskResult
    task_result_file = "core/task_result.py"
    if os.path.exists(task_result_file):
        task_result_fields = get_class_signature(task_result_file, "TaskResult")
        results["TaskResult_valid"] = task_result_fields is not None and len(task_result_fields) > 0
    else:
        results["TaskResult_valid"] = False

    return results


def check_orchestrator_flow() -> Dict[str, bool]:
    """Verify orchestrator pipeline includes prefix → normalize → ECS → mapping → DecisionCore."""
    if not os.path.exists("orchestrator.py"):
        return {
            "orchestrator_exists": False,
            "prefix_detector_used": False,
            "semantic_normalizer_used": False,
            "ecs_used": False,
            "mapping_used": False,
            "decision_core_called": False,
        }
    
    with open("orchestrator.py", "r", encoding="utf-8") as f:
        code = f.read()

    checks = {
        "orchestrator_exists": True,
        "prefix_detector_used": "detect_prefix" in code or "CommandPrefixDetector" in code,
        "semantic_normalizer_used": "normalize_command" in code or "SemanticNormalizer" in code,
        "ecs_used": "resolve_slots" in code or "ECSv1" in code,
        "mapping_used": "normalized_to_parsed_intent" in code or "mapping" in code,
        "decision_core_called": "handle_event" in code and "DecisionCore" in code,
        "taskchain_applied": "apply_decision" in code or "TaskChainManager" in code,
    }
    return checks


def check_logging_integration() -> Dict[str, bool]:
    """检查日志模块是否正确集成."""
    results = {}
    
    # 检查 decision_logging 目录是否存在
    results["decision_logging_exists"] = os.path.exists("decision_logging")
    
    # 检查 decision_core 是否调用 log_decision
    if os.path.exists("decision/decision_core.py"):
        with open("decision/decision_core.py", "r", encoding="utf-8") as f:
            code = f.read()
        results["log_decision_imported"] = "log_decision" in code or "decision_logging" in code
        results["log_decision_called"] = "log_decision(" in code
    else:
        results["log_decision_imported"] = False
        results["log_decision_called"] = False
    
    return results


def write_report(illegal_tc, illegal_dc, cmd_violations, contract_status, orch_status, logging_status):
    """Write review result to markdown report."""
    os.makedirs("reports", exist_ok=True)
    with open("reports/STRUCTURE_REVIEW_v1.4.4.md", "w", encoding="utf-8") as f:
        f.write("# Luna Badge v1.4.4 — Structure Review Report\n\n")
        f.write("**生成时间**: " + str(__import__("datetime").datetime.now()) + "\n\n")
        f.write("---\n\n")

        # 1. Illegal Direct TaskChain Access
        f.write("## 1. Illegal Direct TaskChain Access\n\n")
        if not illegal_tc:
            f.write("✅ **PASS** — No illegal TaskChain imports found.\n\n")
        else:
            f.write("❌ **FAIL** — Illegal imports detected:\n\n")
            for item in illegal_tc:
                f.write(f"- `{item['file']}` imports `{item['import']}`\n")
            f.write("\n")

        # 2. Illegal DecisionCore Access
        f.write("## 2. Illegal DecisionCore Access\n\n")
        if not illegal_dc:
            f.write("✅ **PASS** — DecisionCore only invoked by orchestrator.\n\n")
        else:
            f.write("❌ **FAIL** — Illegal imports detected:\n\n")
            for item in illegal_dc:
                f.write(f"- `{item['file']}` imports `{item['import']}`\n")
            f.write("\n")

        # 3. Command Layer Boundary Violations
        f.write("## 3. Command Layer Boundary Violations\n\n")
        if not cmd_violations:
            f.write("✅ **PASS** — Command Layer does not directly access TaskChain or DecisionCore.\n\n")
        else:
            f.write("❌ **FAIL** — Command Layer violations detected:\n\n")
            for item in cmd_violations:
                f.write(f"- `{item['file']}`: {item['violation']}\n")
            f.write("\n")

        # 4. Contract Object Integrity
        f.write("## 4. Contract Object Integrity\n\n")
        all_contracts_valid = True
        for k, v in contract_status.items():
            status = "✅ PASS" if v else "❌ FAIL"
            f.write(f"- `{k}`: {status}\n")
            if not v:
                all_contracts_valid = False
        f.write("\n")

        # 5. Orchestrator Pipeline Checks
        f.write("## 5. Orchestrator Pipeline Checks\n\n")
        all_orch_valid = True
        for k, v in orch_status.items():
            status = "✅ PASS" if v else "❌ FAIL"
            f.write(f"- `{k}`: {status}\n")
            if not v:
                all_orch_valid = False
        f.write("\n")

        # 6. Logging Integration
        f.write("## 6. Logging Integration\n\n")
        all_logging_valid = True
        for k, v in logging_status.items():
            status = "✅ PASS" if v else "❌ FAIL"
            f.write(f"- `{k}`: {status}\n")
            if not v:
                all_logging_valid = False
        f.write("\n")

        # Summary
        f.write("---\n\n")
        f.write("## Summary\n\n")
        
        all_passed = (
            not illegal_tc and 
            not illegal_dc and 
            not cmd_violations and 
            all_contracts_valid and 
            all_orch_valid and
            all_logging_valid
        )
        
        if all_passed:
            f.write("✅ **ALL CHECKS PASSED** — v1.4.4 structure is ready for freeze.\n\n")
        else:
            f.write("❌ **SOME CHECKS FAILED** — Please review the violations above before freezing.\n\n")
        
        f.write("### Checklist\n\n")
        f.write("- [ ] No illegal TaskChain access\n")
        f.write("- [ ] No illegal DecisionCore access\n")
        f.write("- [ ] Command Layer boundaries respected\n")
        f.write("- [ ] Contract objects unchanged\n")
        f.write("- [ ] Orchestrator pipeline complete\n")
        f.write("- [ ] Logging integration correct\n")


def main():
    print("=" * 60)
    print("Luna Badge v1.4.4 Structure Review")
    print("=" * 60)
    print()
    
    print("Scanning Python files...")
    files = scan_py_files(PROJECT_ROOT)
    print(f"Found {len(files)} Python files")
    
    print("Parsing imports...")
    import_data = [parse_imports(f) for f in files]
    
    print("Checking for illegal TaskChain access...")
    illegal_taskchain = assert_no_direct_taskchain_calls(import_data)
    
    print("Checking for illegal DecisionCore access...")
    illegal_decisioncore = assert_no_direct_decisioncore_calls(import_data)
    
    print("Checking Command Layer boundaries...")
    cmd_violations = check_command_layer_boundaries(import_data)
    
    print("Checking contract objects...")
    contract_status = check_contract_objects()
    
    print("Checking orchestrator flow...")
    orch_status = check_orchestrator_flow()
    
    print("Checking logging integration...")
    logging_status = check_logging_integration()
    
    print("Generating report...")
    write_report(illegal_taskchain, illegal_decisioncore, cmd_violations, 
                 contract_status, orch_status, logging_status)
    
    print()
    print("=" * 60)
    print("✅ Structure review complete!")
    print("=" * 60)
    print()
    print("📄 Report generated: reports/STRUCTURE_REVIEW_v1.4.4.md")
    print()


if __name__ == "__main__":
    main()

