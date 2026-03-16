import express from "express";
import multer from "multer";
import path from "path";
import fs from "fs";
import { runPython } from "../services/python_runner";

const router = express.Router();

const uploadsDir = path.resolve(__dirname, "../../uploads");

if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

const upload = multer({
  dest: uploadsDir,
});

router.post("/", upload.single("video"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: "No video uploaded",
      });
    }

    const videoPath = path.resolve(req.file.path);

    console.log("[/analyze] Uploaded file:");
    console.log("  originalname:", req.file.originalname);
    console.log("  mimetype:", req.file.mimetype);
    console.log("  saved path:", videoPath);

    const result = await runPython(videoPath);

    console.log("[/analyze] Python result:", result);

    return res.status(200).json(result);
  } catch (err: any) {
    console.error("[/analyze] ERROR:", err);

    return res.status(500).json({
      success: false,
      error: String(err),
    });
  }
});

export default router;