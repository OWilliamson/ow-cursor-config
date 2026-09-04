# Customer explanation examples

Internal notes → customer-ready output. Patterns for `/owcc-customer-explanation`.

---

## Answer mode

**Internal context (do not send):**

> Customer asks if Geneos OTel plugin supports full trace spans in dataviews. Jira GENOS-8842 — traces partial; golden metrics from spans only; no span data model yet. Confluence "OTel plugin status" draft.

**Customer text:**

Geneos ingests OpenTelemetry traces and derives golden metrics from each span. Full span objects are not shown in dataviews in the current release — you see the extracted metrics, not the raw span tree.

Metrics and logs are fully supported. For mapping configuration and examples, see the [OpenTelemetry mappings](https://docs.itrsgroup.com/docs/geneos/collection/opentelemetry/current/user-guide/opentelemetry/index.html#mappings) section of the Geneos documentation.

---

## Capability mode

**Internal context (do not send):**

> Explain Opsview Timeseries Graphing Engine to customer. Internal: uses RRD + new engine behind feature flag in 6.9.

**Customer text:**

**Timeseries Graphing Engine** — stores and serves time-series data for Opsview graphs and dashboards.

- Collects check performance and custom metric data from your monitoring infrastructure.
- Powers Graph Center and dashboard dashlets that plot historical values.

Graphing behaviour and administration options are described in the [Timeseries Graphing Engine](https://docs.itrsgroup.com/docs/opsview/current/administration/graphing-data-engine/index.html) documentation.

---

## How-to mode

**Internal context (do not send):**

> Customer needs steps to install IA on RHEL via rpm. We know 2.11.0 supports RHEL 9 — use internal packaging doc path.

**Customer text:**

**Install the Infrastructure Agent on RHEL (RPM)**

**Before you start:** Confirm your RHEL major version is in the supported OS list for your Agent release.

1. Download the `.rpm` package for your OS and architecture from ITRS Downloads.
2. Install the package with your host's package manager.
3. Configure the Agent to communicate with your monitoring system (host, port, and credentials as required by your environment).
4. Start the Agent service and confirm it is running.

**Confirm:** Your monitoring system receives test results from the host.

Supported platforms and network requirements are listed under [Supported versions](https://docs.itrsgroup.com/docs/infrastructure-agent/current/prerequisites/prerequisites/index.html#supported-versions) in the Infrastructure Agent documentation.

---

## Link anti-patterns

**Bad** (backticks, duplicate, pinned version, no anchor):

```markdown
See `https://docs.itrsgroup.com/docs/geneos/collection/opentelemetry/6.2.0/user-guide/opentelemetry/index.html` for setup. Mappings: `https://docs.itrsgroup.com/docs/geneos/collection/opentelemetry/6.2.0/user-guide/opentelemetry/index.html`.
```

**Good:**

```markdown
Setup and mapping examples are in the [OpenTelemetry mappings](https://docs.itrsgroup.com/docs/geneos/collection/opentelemetry/current/user-guide/opentelemetry/index.html#mappings) section of the Geneos documentation.
```

---

## Uncertainty note (to user only)

When the draft is mostly ready but one fact is unverified, end the **agent reply** (not the customer block) with:

> **Before sending:** I could not verify whether X applies on Y — confirm against the customer's Opsview version.
