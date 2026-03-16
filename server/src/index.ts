import express from "express"
import analyze from "./routes/analyze"

const app = express()

app.use(express.json())

app.use("/analyze", analyze)

app.listen(3000, () => {
  console.log("Server running on port 3000")
})