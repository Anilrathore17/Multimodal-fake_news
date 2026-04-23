import { useMemo, useState } from "react";

import { analyze } from "./lib/api";
import { Dropzone } from "./components/Dropzone";
import { LoadingSpinner } from "./components/LoadingSpinner";
import { ResultCard } from "./components/ResultCard";

export default function App() {
  const [text, setText] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{
    prediction: string;
    confidence: number;
    explanation: string;
  } | null>(null);

  const canSubmit = useMemo(() => text.trim().length > 0 && !isLoading, [text, isLoading]);

  async function onSubmit() {
    setError(null);
    setResult(null);
    setIsLoading(true);
    try {
      const res = await analyze({ text, image });
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <header className="mb-8 flex items-end justify-between gap-6">
          <div>
            <div className="text-sm font-medium tracking-widest text-zinc-400">
              MULTIMODAL FAKE NEWS DETECTION
            </div>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">NewsGuard AI</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">
              Submit news text (and optionally an image). The backend runs text analysis, image checks, and
              multimodal fusion to produce a verdict with explanation.
            </p>
          </div>
          <div className="rounded-md border border-zinc-800 bg-zinc-900/30 px-3 py-2 text-xs text-zinc-400">
            API: <span className="text-zinc-200">POST /analyze</span>
          </div>
        </header>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <section className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-5">
            <div className="text-xs font-semibold tracking-widest text-zinc-400">INPUT</div>

            <label className="mt-4 block text-sm font-medium text-zinc-200">News text</label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste headline or full article text…"
              className="mt-2 h-44 w-full resize-none rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 py-2 text-sm outline-none ring-0 placeholder:text-zinc-600 focus:border-zinc-700"
            />

            <div className="mt-4">
              <label className="block text-sm font-medium text-zinc-200">Optional image</label>
              <div className="mt-2">
                <Dropzone
                  file={image}
                  onFile={(f) => setImage(f)}
                  onClear={() => setImage(null)}
                />
              </div>
            </div>

            <button
              type="button"
              onClick={onSubmit}
              disabled={!canSubmit}
              className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-3 text-sm font-semibold tracking-wide text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:bg-zinc-800 disabled:text-zinc-500"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner />
                  Analyzing…
                </>
              ) : (
                "Verify this news"
              )}
            </button>

            {error && (
              <div className="mt-4 rounded-lg border border-red-900/50 bg-red-950/30 px-3 py-2 text-sm text-red-200">
                {error}
              </div>
            )}
          </section>

          <section className="rounded-xl border border-zinc-800 bg-zinc-900/20 p-5">
            <div className="text-xs font-semibold tracking-widest text-zinc-400">RESULT</div>
            <div className="mt-4">
              {result ? (
                <ResultCard
                  prediction={result.prediction}
                  confidence={result.confidence}
                  explanation={result.explanation}
                />
              ) : (
                <div className="flex min-h-[320px] items-center justify-center rounded-lg border border-dashed border-zinc-800 bg-zinc-950/40 px-6 text-center text-sm text-zinc-500">
                  Submit an article to see the verification report here.
                </div>
              )}
            </div>
          </section>
        </div>

        <footer className="mt-10 flex flex-wrap items-center justify-between gap-3 border-t border-zinc-900 pt-6 text-xs text-zinc-500">
          <div>Local dev: frontend on :5173, backend on :8000</div>
          <div className="text-zinc-600">HF explanations are optional via <span className="text-zinc-400">HF_API_TOKEN</span></div>
        </footer>
      </div>
    </div>
  );
}
