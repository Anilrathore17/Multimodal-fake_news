function badgeClasses(prediction: string) {
  const p = prediction.toLowerCase();
  if (p.includes("fake")) return "bg-red-600 text-white";
  if (p.includes("real")) return "bg-emerald-600 text-white";
  return "bg-amber-500 text-black";
}

export function ResultCard(props: { prediction: string; confidence: number; explanation: string }) {
  const pct = Math.round(Math.max(0, Math.min(1, props.confidence)) * 100);

  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-950/40 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${badgeClasses(props.prediction)}`}>
            {props.prediction}
          </span>
          <span className="text-xs text-zinc-500">Confidence</span>
          <span className="text-sm font-semibold text-zinc-200">{pct}%</span>
        </div>
      </div>

      <div className="mt-3 h-2 overflow-hidden rounded-full bg-zinc-900">
        <div className="h-2 rounded-full bg-zinc-200" style={{ width: `${pct}%` }} />
      </div>

      <div className="mt-4">
        <div className="text-xs font-semibold tracking-widest text-zinc-400">EXPLANATION</div>
        <div className="mt-2 whitespace-pre-wrap text-sm leading-6 text-zinc-200">{props.explanation}</div>
      </div>
    </div>
  );
}

