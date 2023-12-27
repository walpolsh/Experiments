import express from "express";
import Ffmpeg from "fluent-ffmpeg";

const app = express();
app.use(express.json());
app.post("/process-video", (req, res) => {
  const inputVideoPath = req.body.inputVideoPath;
  const outputVideoPath = req.body.outputVideoPath;
  if (!inputVideoPath || !outputVideoPath) {
    res.status(400).send("Bad Request: Missing File Path");
  }

  Ffmpeg(inputVideoPath)
    .outputOptions("-vf", "scale=-1:360") // -video format, scale to 360p
    .on("end", () => {
      return res.status(200).send("Video successfully processed.");
    })

    .on("error", (err) => {
      console.log(`An error occured: ${err.message}`);
      res.status(500).send("Internal Server Error");
    })
    .save(outputVideoPath);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Video processing service listening on port ${port}`);
});
