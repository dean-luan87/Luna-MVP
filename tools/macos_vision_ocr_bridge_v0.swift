import Foundation
import Vision
import ImageIO

struct Candidate: Codable {
    let text: String
    let confidence: Double?
    let bbox: [Double]? // [x1,y1,x2,y2] in pixels, y down
}

struct Output: Codable {
    let ok: Bool
    let error: String?
    let error_domain: String?
    let error_code: Int?
    let error_description: String?
    let image_width: Int?
    let image_height: Int?
    let candidates: [Candidate]
}

func bboxToPixels(_ bb: CGRect, w: Int, h: Int) -> [Double] {
    // Vision normalized bb: origin at lower-left
    let x1 = bb.origin.x * Double(w)
    let x2 = (bb.origin.x + bb.size.width) * Double(w)
    let y1 = (1.0 - (bb.origin.y + bb.size.height)) * Double(h)
    let y2 = (1.0 - bb.origin.y) * Double(h)
    return [x1, y1, x2, y2]
}

func loadCGImage(path: String) throws -> (CGImage, Int, Int) {
    let url = URL(fileURLWithPath: path)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil) else {
        throw NSError(domain: "bridge", code: 1, userInfo: [NSLocalizedDescriptionKey: "CGImageSourceCreateWithURL failed"])
    }
    guard let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
        throw NSError(domain: "bridge", code: 2, userInfo: [NSLocalizedDescriptionKey: "CGImageSourceCreateImageAtIndex failed"])
    }
    return (img, img.width, img.height)
}

let args = CommandLine.arguments
if args.count < 2 {
    let out = Output(ok: false, error: "missing_image_path", error_domain: nil, error_code: nil, error_description: nil, image_width: nil, image_height: nil, candidates: [])
    print(String(data: try JSONEncoder().encode(out), encoding: .utf8)!)
    exit(2)
}

let imagePath = args[1]

do {
    let (cgimg, w, h) = try loadCGImage(path: imagePath)

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false

    let handler = VNImageRequestHandler(cgImage: cgimg, options: [:])
    try handler.perform([request])

    let observations = (request.results as? [VNRecognizedTextObservation]) ?? []
    var cands: [Candidate] = []
    cands.reserveCapacity(observations.count)

    for obs in observations {
        let top = obs.topCandidates(1).first
        let text = top?.string ?? ""
        let conf = top != nil ? Double(top!.confidence) : nil
        let bb = bboxToPixels(obs.boundingBox, w: w, h: h)
        cands.append(Candidate(text: text, confidence: conf, bbox: bb))
    }

    let out = Output(ok: true, error: nil, error_domain: nil, error_code: nil, error_description: nil, image_width: w, image_height: h, candidates: cands)
    print(String(data: try JSONEncoder().encode(out), encoding: .utf8)!)
    exit(0)
} catch {
    let ns = error as NSError
    let out = Output(
        ok: false,
        error: String(describing: error),
        error_domain: ns.domain,
        error_code: ns.code,
        error_description: ns.localizedDescription,
        image_width: nil,
        image_height: nil,
        candidates: []
    )
    print(String(data: try JSONEncoder().encode(out), encoding: .utf8)!)
    exit(1)
}

