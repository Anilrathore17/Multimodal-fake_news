import { useCallback, useRef, useState } from "react";

type Props = {
  file: File | null;
  onFile: (f: File) => void;
  onClear: () => void;
};

const ACCEPTED = ["image/jpeg", "image/png", "image/webp"];

export function Dropzone({ file, onFile, onClear }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const pick = useCallback(() => inputRef.current?.click(), []);

  const onDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const f = e.dataTransfer.files?.[0];
      if (!f) return;
      if (!ACCEPTED.includes(f.type)) return;
      onFile(f);
    },
    [onFile]
  );

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept=".jpg,.jpeg,.png,.webp"
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (!f) return;
          onFile(f);
        }}
      />

      <div
        onClick={pick}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        className={[
          "cursor-pointer rounded-lg border border-dashed px-4 py-4 text-sm transition",
          isDragging ? "border-zinc-500 bg-zinc-900/40" : "border-zinc-800 bg-zinc-950/40 hover:border-zinc-700",
        ].join(" ")}
      >
        {file ? (
          <div className="flex items-center justify-between gap-3">
            <div className="min-w-0">
              <div className="truncate font-medium text-zinc-200">{file.name}</div>
              <div className="text-xs text-zinc-500">{Math.round(file.size / 1024)} KB</div>
            </div>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onClear();
              }}
              className="rounded-md border border-zinc-800 bg-zinc-900/20 px-2 py-1 text-xs text-zinc-200 hover:bg-zinc-900/40"
            >
              Remove
            </button>
          </div>
        ) : (
          <div className="text-zinc-400">
            Drag & drop an image here, or <span className="text-zinc-200 underline underline-offset-2">browse</span>
            <div className="mt-1 text-xs text-zinc-600">JPG, PNG, WEBP</div>
          </div>
        )}
      </div>
    </div>
  );
}

