export type AnalyzeResponse = {
  prediction: string;
  confidence: number;
  explanation: string;
};

type AnalyzeInput = {
  text: string;
  image: File | null;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export async function analyze(input: AnalyzeInput): Promise<AnalyzeResponse> {
  const form = new FormData();
  form.append("text", input.text);
  if (input.image) form.append("image", input.image);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: form,
  });

  const contentType = res.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");
  const body = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const detail =
      typeof body === "object" && body && "detail" in body ? String((body as any).detail) : String(body);
    throw new Error(detail || `Request failed (${res.status})`);
  }

  return body as AnalyzeResponse;
}

