import { Storage } from "@google-cloud/storage";
import fs from "fs";
import Ffmpeg from "fluent-ffmpeg";

const storage = new Storage();
const rawVideoBucketName = "pauls-raw-yt-videos";
const processedVideoBucketName = "pauls-processed-yt-videos";

const localRawVideoPath = "./raw-videos";
const localProceesedVideoPath = "./processed-videos";

export function setupDirectories() {
  ensureDirectoryExistance(localRawVideoPath);
  ensureDirectoryExistance(localProceesedVideoPath);
}

export function convertVideo(rawVideoName: string, processedVideoName: string) {
  return new Promise<void>((resolve, reject) => {
    Ffmpeg(`${localRawVideoPath}/${rawVideoName}`)
      .outputOptions("-vf", "scale=-1:360") // -video format, scale to 360p
      .on("end", () => {
        console.log("Video successfully processed.");
        resolve();
      })

      .on("error", (err) => {
        console.log(`An error occured: ${err.message}`);
        reject(err);
      })
      .save(`${localProceesedVideoPath}/${processedVideoName}`);
  });
}

export async function downloadRawVideo(fileName: string) {
  await storage
    .bucket(rawVideoBucketName)
    .file(fileName)
    .download({ destination: `${localRawVideoPath}/${fileName}` });
  console.log(`gs://${rawVideoBucketName}/${fileName} downloaded to ${localRawVideoPath}/${fileName}`);
}

export async function uploadProcessedVideo(fileName: string) {
  const bucket = storage.bucket(processedVideoBucketName);
  bucket.upload(`${localProceesedVideoPath}/${fileName}`, {
    destination: fileName,
  });
  console.log(`gs://${localProceesedVideoPath}/${fileName} downloaded to ${processedVideoBucketName}/${fileName}`);

  await bucket.file(fileName).makePublic();
}

function deleteFile(filePath: string): Promise<void> {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(filePath)) {
      fs.unlink(filePath, (err) => {
        if (err) {
          console.log(`Failed to delete file at ${filePath}`, err);
          reject(err);
        } else {
          console.log(`File deleteed at ${filePath}`, err);
        }
      });
    } else {
      console.log(`File not found at ${filePath}, skipping deletion.`);
      resolve();
    }
  });
}

export function deleteRawVideo(fileName: string) {
  return deleteFile(`${localRawVideoPath}/${fileName}`);
}

export function deleteProcessedVideo(fileName: string) {
  return deleteFile(`${localRawVideoPath}/${fileName}`);
}

function ensureDirectoryExistance(dirPath: string) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Directory created at ${dirPath}`);
  }
}
