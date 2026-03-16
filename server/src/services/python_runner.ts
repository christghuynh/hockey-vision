import { spawn } from "child_process"
import path from "path"

export function runPython(videoPath: string): Promise<any> {
  return new Promise((resolve, reject) => {
    const script = path.resolve(__dirname, "../../../scripts/process_session.py")
    const pythonExe = path.resolve(__dirname, "../../../venv/Scripts/python.exe")

    console.log("USING PYTHON EXE:", pythonExe)
    console.log("USING SCRIPT:", script)
    console.log("VIDEO PATH:", videoPath)

    const python = spawn(pythonExe, [script, videoPath])

    let output = ""
    let error = ""

    python.stdout.on("data", (data) => {
      output += data.toString()
    })

    python.stderr.on("data", (data) => {
      error += data.toString()
    })

    python.on("close", (code) => {
      console.log("PYTHON EXIT CODE:", code)
      console.log("RAW PYTHON STDOUT:", output)
      console.log("RAW PYTHON STDERR:", error)

      if (code !== 0) {
        return reject(error || `Python exited with code ${code}`)
      }

      try {
        const parsed = JSON.parse(output)
        resolve(parsed)
      } catch {
        reject(`Invalid JSON from Python. STDOUT was: ${output}`)
      }
    })

    python.on("error", (err) => {
      reject(`Failed to start Python process: ${err.message}`)
    })
  })
}