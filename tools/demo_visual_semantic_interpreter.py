from visual_semantic_interpreter.v1_rule_based import RuleBasedInterpreterV1
from visual_semantic_interpreter.types import VisualContext, OCRToken, VisualObject


def main():
    ctx = VisualContext(
        roi_kind="exit_area",
        scene_tags=["mall"],
        objects=[],
        ocr_tokens=[
            OCRToken(text="EXIT", bbox=(0, 0, 10, 10), confidence=0.9),
        ],
    )

    interpreter = RuleBasedInterpreterV1()
    result = interpreter.interpret(ctx)

    for i in result.interpretations:
        print(i)


if __name__ == "__main__":
    main()
