import express from "express";
import cors from "cors";
import path from "path";
import analyze from "./routes/analyze";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/outputs", express.static(path.resolve(__dirname, "../../outputs")));
app.use("/analyze", analyze);

app.listen(3000, () => {
  console.log("Server running on port 3000");
});