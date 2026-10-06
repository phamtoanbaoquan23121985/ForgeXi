// ForgeXi native WebMCP producer. No credentials are available to this module.
export async function registerForgeXiTools(api, signal) {
  const mc = document.modelContext;
  if (!mc?.registerTool) return { supported: false, registered: [] };

  const specs = [
    ["probe_models", "Probe configured ForgeXi model availability without inference.", {
      type: "object", properties: {}, additionalProperties: false
    }, true],
    ["run_nemotron_decision", "Run one bounded Nemotron decision through the ForgeXi runtime.", {
      type: "object",
      properties: { prompt: { type: "string", minLength: 1, maxLength: 4000 } },
      required: ["prompt"], additionalProperties: false
    }, false],
    ["run_forgexi_task", "Run a bounded ForgeXi software task through plan, act, test, repair and verify.", {
      type: "object",
      properties: {
        task: { type: "string", minLength: 1, maxLength: 4000 },
        max_repairs: { type: "integer", minimum: 0, maximum: 5, default: 2 }
      },
      required: ["task"], additionalProperties: false
    }, false],
    ["get_run_status", "Read the status of a ForgeXi run.", {
      type: "object",
      properties: { run_id: { type: "string", minLength: 1, maxLength: 128 } },
      required: ["run_id"], additionalProperties: false
    }, true],
    ["get_evidence_receipt", "Read the secret-free verification receipt for a ForgeXi run.", {
      type: "object",
      properties: { run_id: { type: "string", minLength: 1, maxLength: 128 } },
      required: ["run_id"], additionalProperties: false
    }, true],
  ];

  const registered = [];
  for (const [name, description, inputSchema, readOnlyHint] of specs) {
    await mc.registerTool({
      name, description, inputSchema,
      annotations: { readOnlyHint, untrustedContentHint: false },
      execute: async (input, options = {}) => {
        if (options.signal?.aborted) throw new DOMException("Aborted", "AbortError");
        return await api.invoke(name, input, { signal: options.signal });
      },
    }, { signal });
    registered.push(name);
  }
  return { supported: true, registered };
}
