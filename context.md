# ContextPack — Project Summary

## Metadata

| Field | Value |
|-------|-------|
| Language | TypeScript |
| Framework | Ink |
| Architectural Pattern | Microservice, CLI Tool, MVC, Machine Learning |
| Entry Point | C:/Users/Sasha/gemini-cli\packages\sdk\index.ts |
| Total Files | 857 |
| Dependencies | ink, latest-version, node-fetch-native, proper-lockfile, punycode, simple-git |
| Dev Dependencies | @agentclientprotocol/sdk, @octokit/rest, @types/marked, @types/mime-types, @types/minimatch, @types/mock-fs, @types/prompts, @types/proper-lockfile, @types/react, @types/react-dom, @types/shell-quote, @types/ws, @vitest/coverage-v8, @vitest/eslint-plugin, cross-env, depcheck, domexception, esbuild, esbuild-plugin-wasm, eslint, eslint-config-prettier, eslint-plugin-headers, eslint-plugin-import, eslint-plugin-react, eslint-plugin-react-hooks, glob, globals, google-artifactregistry-auth, husky, json, lint-staged, memfs, mnemonist, mock-fs, msw, npm-run-all, prettier, react-devtools-core, react-dom, semver, strip-ansi, ts-prune, tsx, typescript-eslint, vitest, yargs |

## Key Files

### `C:/Users/Sasha/gemini-cli\packages\sdk\index.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

export * from './src/index.js';

> Provides a lightweight, local client for real-time language model interactions.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\core\localLiteRtLmClient.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { GoogleGenAI, type Content } from '@google/genai';
import type { Config } from '../config/config.js';
import { debugLogger } from '../utils/debugLogger.js';

/**
 * A client for making single, non-streaming calls to a local Gemini-compatible API
 * and expecting a JSON response.
 */
export class LocalLiteRtLmClient {
  private readonly host: string;
  private readonly model: string;
  private readonly client: GoogleGenAI;

  constructor(config: Config) {
    const gemmaModelRouterSettings = config.getGemmaModelRouterSettings();
    this.host = gemmaModelRouterSettings.classifier!.host!;
    this.model = gemmaModelRouterSettings.classifier!.model!;

    this.client = new GoogleGenAI({
      // The LiteRT-LM server does not require an API key, but the SDK requires one to be set even for local endpoints. This is a dummy value and is not used for authentication.
      apiKey: 'no-api-key-needed',
      httpOptions: {
        baseUrl: this.host,
        // If the LiteRT-LM server is started but the wrong port is set, there will be a lengthy TCP timeout (here fixed to be 10 seconds).
        // If the LiteRT-LM server is not started, there will be an immediate connection refusal.
        // If the LiteRT-LM server is started and the model is unsupported or not downloaded, the server will return an error immediately.
        // If the model's context window is exceeded, the server will return an error immediately.
        timeout: 10000,
      },
    });
  }

  /**
   * Sends a prompt to the local Gemini model and expects a JSON object in response.
   * @param contents The history and current prompt.
   * @param systemInstruction The system prompt.
   * @returns A promise that resolves to the parsed JSON object.
   */
  async generateJson(
    contents: Content[],
    systemInstruction: string,
    reminder?: string,
    abortSignal?: AbortSignal,
  ): Promise<object> {

> Main entry point for the Gemini command-line interface application.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\index.ts`
```typescript
#!/usr/bin/env -S node --no-warnings=DEP0040

/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

// --- Fast Path for Version ---
// We check for version flags at the very top to avoid loading any heavy dependencies.
// process.env.CLI_VERSION is defined during the build process by esbuild.
if (process.argv.includes('--version') || process.argv.includes('-v')) {
  console.log(process.env['CLI_VERSION'] || 'unknown');
  process.exit(0);
}

// --- Global Entry Point ---

let writeToStderrFn: (message: string) => void = (msg) =>
  process.stderr.write(msg);

// Suppress known race condition error in node-pty on Windows
// Tracking bug: https://github.com/microsoft/node-pty/issues/827
process.on('uncaughtException', (error) => {
  if (
    process.platform === 'win32' &&
    error instanceof Error &&
    error.message === 'Cannot resize a pty that has already exited'
  ) {
    // This error happens on Windows with node-pty when resizing a pty that has just exited.
    // It is a race condition in node-pty that we cannot prevent, so we silence it.
    return;
  }

  // For other errors, we rely on the default behavior, but since we attached a listener,
  // we must manually replicate it.
  if (error instanceof Error) {
    writeToStderrFn(error.stack + '\n');
  } else {
    writeToStderrFn(String(error) + '\n');
  }
  process.exit(1);
});

const [{ main }, { FatalError, writeToStderr }, { runExitCleanup }] =
  await Promise.all([
    import('./src/gemini.js'),
    import('@google/gemini-cli-core'),
    import('./src/utils/cleanup.js'),
  ]);

> Exports core functionalities and shared utilities for the application.
```

### `C:/Users/Sasha/gemini-cli\packages\core\index.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

export * from './src/index.js';
export { Storage } from './src/config/storage.js';
export {
  DEFAULT_GEMINI_MODEL,
  DEFAULT_GEMINI_MODEL_AUTO,
  DEFAULT_GEMINI_FLASH_MODEL,
  DEFAULT_GEMINI_FLASH_LITE_MODEL,
  DEFAULT_GEMINI_EMBEDDING_MODEL,
} from './src/config/models.js';
export {
  serializeTerminalToObject,
  type AnsiOutput,
  type AnsiLine,
  type AnsiToken,
} from './src/utils/terminalSerializer.js';
export { DEFAULT_TRUNCATE_TOOL_OUTPUT_THRESHOLD } from './src/config/config.js';
export { detectIdeFromEnv } from './src/ide/detect-ide.js';
export {
  logExtensionEnable,
  logIdeConnection,
  logExtensionDisable,
} from './src/telemetry/loggers.js';

export {
  IdeConnectionEvent,
  IdeConnectionType,
  ExtensionInstallEvent,
  ExtensionDisableEvent,
  ExtensionEnableEvent,
  ExtensionUninstallEvent,
  ExtensionUpdateEvent,
  ModelSlashCommandEvent,
} from './src/telemetry/types.js';
export { makeFakeConfig } from './src/test-utils/config.js';
export * from './src/utils/pathReader.js';
export { ClearcutLogger } from './src/telemetry/clearcut-logger/clearcut-logger.js';
export { logModelSlashCommand } from './src/telemetry/loggers.js';
export { KeychainTokenStorage } from './src/mcp/token-storage/keychain-token-storage.js';
export * from './src/utils/googleQuotaErrors.js';
export type { GoogleApiError } from './src/utils/googleErrors.js';
export { getCodeAssistServer } from './src/code_assist/codeAssist.js';
export { getExperiments } from './src/code_assist/experiments/experiments.js';
export { ExperimentFlags } from './src/code_assist/experiments/flagNames.js';
export { getErrorStatus, ModelNotFoundError } from './src/utils/httpErrors.js';

> Defines a routing strategy that requires user approval for operations.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\routing\strategies\approvalModeStrategy.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type { Config } from '../../config/config.js';
import {
  isAutoModel,
  resolveClassifierModel,
  GEMINI_MODEL_ALIAS_FLASH,
  GEMINI_MODEL_ALIAS_PRO,
} from '../../config/models.js';
import type { BaseLlmClient } from '../../core/baseLlmClient.js';
import { ApprovalMode } from '../../policy/types.js';
import type {
  RoutingContext,
  RoutingDecision,
  RoutingStrategy,
} from '../routingStrategy.js';

/**
 * A strategy that routes based on the current ApprovalMode and plan status.
 *
 * - In PLAN mode: Routes to the PRO model for high-quality planning.
 * - In other modes with an approved plan: Routes to the FLASH model for efficient implementation.
 */
export class ApprovalModeStrategy implements RoutingStrategy {
  readonly name = 'approval-mode';

  async route(
    context: RoutingContext,
    config: Config,
    _baseLlmClient: BaseLlmClient,
  ): Promise<RoutingDecision | null> {
    const model = context.requestedModel ?? config.getModel();

    // This strategy only applies to "auto" models.
    if (!isAutoModel(model, config)) {
      return null;
    }

    if (!(await config.getPlanModeRoutingEnabled())) {
      return null;
    }

    const startTime = Date.now();
    const approvalMode = config.getApprovalMode();
    const approvedPlanPath = config.getApprovedPlanPath();

> Consolidates and re-exports internal core modules for the package.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\index.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

// Export config
export * from './config/config.js';
export * from './config/agent-loop-context.js';
export * from './config/memory.js';
export * from './config/defaultModelConfigs.js';
export * from './config/models.js';
export * from './config/constants.js';
export * from './output/types.js';
export * from './output/json-formatter.js';
export * from './output/stream-json-formatter.js';
export * from './policy/types.js';
export * from './policy/policy-engine.js';
export * from './policy/toml-loader.js';
export * from './policy/config.js';
export * from './policy/integrity.js';
export * from './config/extensions/integrity.js';
export * from './config/extensions/integrityTypes.js';
export * from './billing/index.js';
export * from './confirmation-bus/types.js';
export * from './confirmation-bus/message-bus.js';

// Export Commands logic
export * from './commands/extensions.js';
export * from './commands/restore.js';
export * from './commands/init.js';
export * from './commands/memory.js';
export * from './commands/types.js';

// Export Core Logic
export * from './core/baseLlmClient.js';
export * from './core/client.js';
export * from './core/contentGenerator.js';
export * from './core/loggingContentGenerator.js';
export * from './core/geminiChat.js';
export * from './core/logger.js';
export * from './core/prompts.js';
export * from './core/tokenLimits.js';
export * from './core/turn.js';
export * from './core/geminiRequest.js';
export * from './scheduler/scheduler.js';
export * from './scheduler/types.js';
export * from './scheduler/tool-executor.js';
export * from './core/recordingContentGenerator.js';

> Wraps and integrates external tools for use by subagents.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\agents\subagent-tool-wrapper.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  BaseDeclarativeTool,
  Kind,
  type ToolInvocation,
  type ToolResult,
} from '../tools/tools.js';

import { type AgentLoopContext } from '../config/agent-loop-context.js';
import type { AgentDefinition, AgentInputs } from './types.js';
import { LocalSubagentInvocation } from './local-invocation.js';
import { RemoteAgentInvocation } from './remote-invocation.js';
import { BrowserAgentInvocation } from './browser/browserAgentInvocation.js';
import { BROWSER_AGENT_NAME } from './browser/browserAgentDefinition.js';
import type { MessageBus } from '../confirmation-bus/message-bus.js';

/**
 * A tool wrapper that dynamically exposes a subagent as a standard,
 * strongly-typed `DeclarativeTool`.
 */
export class SubagentToolWrapper extends BaseDeclarativeTool<
  AgentInputs,
  ToolResult
> {
  /**
   * Constructs the tool wrapper.
   *
   * The constructor dynamically generates the JSON schema for the tool's
   * parameters based on the subagent's input configuration.
   *
   * @param definition The `AgentDefinition` of the subagent to wrap.
   * @param context The execution context.
   * @param messageBus Optional message bus for policy enforcement.
   */
  constructor(
    private readonly definition: AgentDefinition,
    private readonly context: AgentLoopContext,
    messageBus: MessageBus,
  ) {
    super(
      definition.name,
      definition.displayName ?? definition.name,
      definition.description,
      Kind.Agent,
      definition.inputConfig.inputSchema,

> Manages and provides central configuration settings for the core functionality.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\config\config.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import { SandboxPolicyManager } from '../policy/sandboxPolicyManager.js';
import { inspect } from 'node:util';
import process from 'node:process';
import { z } from 'zod';
import {
  AuthType,
  createContentGenerator,
  createContentGeneratorConfig,
  type ContentGenerator,
  type ContentGeneratorConfig,
} from '../core/contentGenerator.js';
import type { OverageStrategy } from '../billing/billing.js';
import { PromptRegistry } from '../prompts/prompt-registry.js';
import { ResourceRegistry } from '../resources/resource-registry.js';
import { ToolRegistry } from '../tools/tool-registry.js';
import { LSTool } from '../tools/ls.js';
import { ReadFileTool } from '../tools/read-file.js';
import { GrepTool } from '../tools/grep.js';
import { canUseRipgrep, RipGrepTool } from '../tools/ripGrep.js';
import { GlobTool } from '../tools/glob.js';
import { ActivateSkillTool } from '../tools/activate-skill.js';
import { EditTool } from '../tools/edit.js';
import { ShellTool } from '../tools/shell.js';
import { WriteFileTool } from '../tools/write-file.js';
import { WebFetchTool } from '../tools/web-fetch.js';
import { MemoryTool, setGeminiMdFilename } from '../tools/memoryTool.js';
import { WebSearchTool } from '../tools/web-search.js';
import { AskUserTool } from '../tools/ask-user.js';
import { ExitPlanModeTool } from '../tools/exit-plan-mode.js';
import { EnterPlanModeTool } from '../tools/enter-plan-mode.js';
import { GeminiClient } from '../core/client.js';
import { BaseLlmClient } from '../core/baseLlmClient.js';
import { LocalLiteRtLmClient } from '../core/localLiteRtLmClient.js';
import type { HookDefinition, HookEventName } from '../hooks/types.js';
import { FileDiscoveryService } from '../services/fileDiscoveryService.js';
import { GitService } from '../services/gitService.js';
import {
  type SandboxManager,
  NoopSandboxManager,
} from '../services/sandboxManager.js';
import { createSandboxManager } from '../services/sandboxManagerFactory.js';
import { SandboxedFileSystemService } from '../services/sandboxedFileSystemService.js';

> Defines configuration settings specifically for the CLI's sandbox environment.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\src\config\sandboxConfig.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  getPackageJson,
  type SandboxConfig,
  FatalSandboxError,
} from '@google/gemini-cli-core';
import commandExists from 'command-exists';
import * as os from 'node:os';
import type { Settings } from './settings.js';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// This is a stripped-down version of the CliArgs interface from config.ts
// to avoid circular dependencies.
interface SandboxCliArgs {
  sandbox?: boolean | string | null;
}
const VALID_SANDBOX_COMMANDS = [
  'docker',
  'podman',
  'sandbox-exec',
  'runsc',
  'lxc',
  'windows-native',
];

function isSandboxCommand(
  value: string,
): value is Exclude<SandboxConfig['command'], undefined> {
  return (VALID_SANDBOX_COMMANDS as ReadonlyArray<string | undefined>).includes(
    value,
  );
}

function getSandboxCommand(
  sandbox?: boolean | string | null,
): SandboxConfig['command'] | '' {
  // If the SANDBOX env var is set, we're already inside the sandbox.
  if (process.env['SANDBOX']) {
    return '';
  }

> Defines the schema and validation rules for CLI application settings.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\src\config\settingsSchema.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

// --------------------------------------------------------------------------
// IMPORTANT: After adding or updating settings, run `npm run docs:settings`
// to regenerate the settings reference in `docs/get-started/configuration.md`.
// --------------------------------------------------------------------------

import {
  DEFAULT_TRUNCATE_TOOL_OUTPUT_THRESHOLD,
  DEFAULT_MODEL_CONFIGS,
  AuthProviderType,
  type MCPServerConfig,
  type RequiredMcpServerConfig,
  type BugCommandSettings,
  type TelemetrySettings,
  type AuthType,
  type AgentOverride,
  type CustomTheme,
  type SandboxConfig,
} from '@google/gemini-cli-core';
import type { SessionRetentionSettings } from './settings.js';
import { DEFAULT_MIN_RETENTION } from '../utils/sessionCleanup.js';

export type SettingsType =
  | 'boolean'
  | 'string'
  | 'number'
  | 'array'
  | 'object'
  | 'enum';

export type SettingsValue =
  | boolean
  | string
  | number
  | string[]
  | object
  | undefined;

/**
 * Setting datatypes that "toggle" through a fixed list of options
 * (e.g. an enum or true/false) rather than allowing for free form input
 * (like a number or string).
 */
export const TOGGLE_TYPES: ReadonlySet<SettingsType | undefined> = new Set([
  'boolean',

> Provides utility functions to manage and facilitate approval mode operations.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\utils\approvalModeUtils.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { ApprovalMode } from '../policy/types.js';
import { checkExhaustive } from './checks.js';

/**
 * Returns a human-readable description for an approval mode.
 */
export function getApprovalModeDescription(mode: ApprovalMode): string {
  switch (mode) {
    case ApprovalMode.AUTO_EDIT:
      return 'Auto-Edit mode (edits will be applied automatically)';
    case ApprovalMode.DEFAULT:
      return 'Default mode (edits will require confirmation)';
    case ApprovalMode.PLAN:
      return 'Plan mode (read-only planning)';
    case ApprovalMode.YOLO:
      return 'YOLO mode (all tool calls auto-approved)';
    default:
      return checkExhaustive(mode);
  }
}

/**
 * Generates a consistent message for plan mode transitions.
 */
export function getPlanModeExitMessage(
  newMode: ApprovalMode,
  isManual: boolean = false,
): string {
  const description = getApprovalModeDescription(newMode);
  const prefix = isManual
    ? 'User has manually exited Plan Mode.'
    : 'Plan approved.';
  return `${prefix} Switching to ${description}.`;
}

> Wraps the MCP tool for use by browser-based agents.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\agents\browser\mcpToolWrapper.ts`
```typescript
/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Creates DeclarativeTool classes for MCP tools.
 *
 * These tools are ONLY registered in the browser agent's isolated ToolRegistry,
 * NOT in the main agent's registry. They dispatch to the BrowserManager's
 * isolated MCP client directly.
 *
 * Tool definitions are dynamically discovered from chrome-devtools-mcp
 * at runtime, not hardcoded.
 */

import type { FunctionDeclaration } from '@google/genai';
import type { Tool as McpTool } from '@modelcontextprotocol/sdk/types.js';
import {
  type ToolConfirmationOutcome,
  DeclarativeTool,
  BaseToolInvocation,
  Kind,
  type ToolResult,
  type ToolInvocation,
  type ToolCallConfirmationDetails,
  type PolicyUpdateOptions,
} from '../../tools/tools.js';
import type { MessageBus } from '../../confirmation-bus/message-bus.js';
import type { BrowserManager, McpToolCallResult } from './browserManager.js';
import { debugLogger } from '../../utils/debugLogger.js';
import { suspendInputBlocker, resumeInputBlocker } from './inputBlocker.js';
import { MCP_TOOL_PREFIX } from '../../tools/mcp-tool.js';
import { BROWSER_AGENT_NAME } from './browserAgentDefinition.js';

/**
 * Tools that interact with page elements and require the input blocker
 * overlay to be temporarily SUSPENDED (pointer-events: none) so
 * chrome-devtools-mcp's interactability checks pass.  The overlay
 * stays in the DOM — only the CSS property toggles, zero flickering.
 */
const INTERACTIVE_TOOLS = new Set([
  'click',
  'click_at',
  'fill',
  'fill_form',
  'hover',
  'drag',
  'upload_file',

> Provides the foundational abstraction for interacting with language models.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\core\baseLlmClient.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type {
  Content,
  Part,
  EmbedContentParameters,
  GenerateContentResponse,
  GenerateContentParameters,
  GenerateContentConfig,
} from '@google/genai';
import type { Config } from '../config/config.js';
import type { ContentGenerator, AuthType } from './contentGenerator.js';
import { handleFallback } from '../fallback/handler.js';
import { getResponseText } from '../utils/partUtils.js';
import { reportError } from '../utils/errorReporting.js';
import { getErrorMessage } from '../utils/errors.js';
import {
  logMalformedJsonResponse,
  logNetworkRetryAttempt,
} from '../telemetry/loggers.js';
import {
  MalformedJsonResponseEvent,
  LlmRole,
  NetworkRetryAttemptEvent,
} from '../telemetry/types.js';
import { retryWithBackoff, getRetryErrorType } from '../utils/retry.js';
import { coreEvents } from '../utils/events.js';
import { getDisplayString } from '../config/models.js';
import type { ModelConfigKey } from '../services/modelConfigService.js';
import {
  applyModelSelection,
  createAvailabilityContextProvider,
} from '../availability/policyHelpers.js';

const DEFAULT_MAX_ATTEMPTS = 5;

/**
 * Options for the generateJson utility function.
 */
export interface GenerateJsonOptions {
  /** The desired model config. */
  modelConfigKey: ModelConfigKey;
  /** The input prompt or history. */
  contents: Content[];
  /** The required JSON schema for the output. */
  schema: Record<string, unknown>;

> Renders the primary content area of the CLI's user interface.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\src\ui\components\MainContent.tsx`
```
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { Box, Static } from 'ink';
import { HistoryItemDisplay } from './HistoryItemDisplay.js';
import { useUIState } from '../contexts/UIStateContext.js';
import { useAppContext } from '../contexts/AppContext.js';
import { AppHeader } from './AppHeader.js';
import { useAlternateBuffer } from '../hooks/useAlternateBuffer.js';
import {
  SCROLL_TO_ITEM_END,
  type VirtualizedListRef,
} from './shared/VirtualizedList.js';
import { ScrollableList } from './shared/ScrollableList.js';
import { useMemo, memo, useCallback, useEffect, useRef } from 'react';
import { MAX_GEMINI_MESSAGE_LINES } from '../constants.js';
import { useConfirmingTool } from '../hooks/useConfirmingTool.js';
import { ToolConfirmationQueue } from './ToolConfirmationQueue.js';

const MemoizedHistoryItemDisplay = memo(HistoryItemDisplay);
const MemoizedAppHeader = memo(AppHeader);

// Limit Gemini messages to a very high number of lines to mitigate performance
// issues in the worst case if we somehow get an enormous response from Gemini.
// This threshold is arbitrary but should be high enough to never impact normal
// usage.
export const MainContent = () => {
  const { version } = useAppContext();
  const uiState = useUIState();
  const isAlternateBuffer = useAlternateBuffer();

  const confirmingTool = useConfirmingTool();
  const showConfirmationQueue = confirmingTool !== null;
  const confirmingToolCallId = confirmingTool?.tool.callId;

  const scrollableListRef = useRef<VirtualizedListRef<unknown>>(null);

  useEffect(() => {
    if (showConfirmationQueue) {
      scrollableListRef.current?.scrollToEnd();
    }
  }, [showConfirmationQueue, confirmingToolCallId]);

  const {
    pendingHistoryItems,
    mainAreaWidth,
    staticAreaMaxItemHeight,

> Displays a dialog for users to input API authentication credentials.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\src\ui\auth\ApiAuthDialog.tsx`
```
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type React from 'react';
import { useRef, useEffect } from 'react';
import { Box, Text } from 'ink';
import { theme } from '../semantic-colors.js';
import { TextInput } from '../components/shared/TextInput.js';
import { useTextBuffer } from '../components/shared/text-buffer.js';
import { useUIState } from '../contexts/UIStateContext.js';
import { clearApiKey, debugLogger } from '@google/gemini-cli-core';
import { useKeypress } from '../hooks/useKeypress.js';
import { Command } from '../key/keyMatchers.js';
import { useKeyMatchers } from '../hooks/useKeyMatchers.js';

interface ApiAuthDialogProps {
  onSubmit: (apiKey: string) => void;
  onCancel: () => void;
  error?: string | null;
  defaultValue?: string;
}

export function ApiAuthDialog({
  onSubmit,
  onCancel,
  error,
  defaultValue = '',
}: ApiAuthDialogProps): React.JSX.Element {
  const keyMatchers = useKeyMatchers();
  const { terminalWidth } = useUIState();
  const viewportWidth = terminalWidth - 8;

  const pendingPromise = useRef<{ cancel: () => void } | null>(null);

  useEffect(
    () => () => {
      pendingPromise.current?.cancel();
    },
    [],
  );

  const initialApiKey = defaultValue;

  const buffer = useTextBuffer({
    initialText: initialApiKey || '',
    initialCursorOffset: initialApiKey?.length || 0,
    viewport: {

> Main entry point for the a2a (agent-to-agent) communication server.
```

### `C:/Users/Sasha/gemini-cli\packages\a2a-server\index.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

export * from './src/index.js';

> An AI agent designed to provide help and guidance for CLI commands.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\agents\cli-help-agent.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type { AgentDefinition } from './types.js';
import { GEMINI_MODEL_ALIAS_FLASH } from '../config/models.js';
import { z } from 'zod';
import { GetInternalDocsTool } from '../tools/get-internal-docs.js';
import type { AgentLoopContext } from '../config/agent-loop-context.js';

const CliHelpReportSchema = z.object({
  answer: z
    .string()
    .describe('The detailed answer to the user question about Gemini CLI.'),
  sources: z
    .array(z.string())
    .describe('The documentation files used to answer the question.'),
});

/**
 * An agent specialized in answering questions about Gemini CLI itself,
 * using its own documentation and runtime state.
 */
export const CliHelpAgent = (
  context: AgentLoopContext,
): AgentDefinition<typeof CliHelpReportSchema> => ({
  name: 'cli_help',
  kind: 'local',
  displayName: 'CLI Help Agent',
  description:
    'Specialized agent for answering questions about the Gemini CLI application. Invoke this agent for questions regarding CLI features, configuration schemas (e.g., policies), or instructions on how to create custom subagents. It queries internal documentation to provide accurate usage guidance.',
  inputConfig: {
    inputSchema: {
      type: 'object',
      properties: {
        question: {
          type: 'string',
          description: 'The specific question about Gemini CLI.',
        },
      },
      required: ['question'],
    },
  },
  outputConfig: {
    outputName: 'report',
    description: 'The final answer and sources as a JSON object.',
    schema: CliHelpReportSchema,
  },

> Implements the server-side logic for code assistance functionalities.
```

### `C:/Users/Sasha/gemini-cli\packages\core\src\code_assist\server.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import type { AuthClient } from 'google-auth-library';
import {
  UserTierId,
  type CodeAssistGlobalUserSettingResponse,
  type LoadCodeAssistRequest,
  type LoadCodeAssistResponse,
  type LongRunningOperationResponse,
  type OnboardUserRequest,
  type SetCodeAssistGlobalUserSettingRequest,
  type ClientMetadata,
  type RetrieveUserQuotaRequest,
  type RetrieveUserQuotaResponse,
  type FetchAdminControlsRequest,
  type FetchAdminControlsResponse,
  type ConversationOffered,
  type ConversationInteraction,
  type StreamingLatency,
  type RecordCodeAssistMetricsRequest,
  type GeminiUserTier,
  type Credits,
} from './types.js';
import type {
  ListExperimentsRequest,
  ListExperimentsResponse,
} from './experiments/types.js';
import type {
  CountTokensParameters,
  CountTokensResponse,
  EmbedContentParameters,
  EmbedContentResponse,
  GenerateContentParameters,
  GenerateContentResponse,
} from '@google/genai';
import * as readline from 'node:readline';
import { Readable } from 'node:stream';
import type { ContentGenerator } from '../core/contentGenerator.js';
import type { Config } from '../config/config.js';
import {
  G1_CREDIT_TYPE,
  getG1CreditBalance,
  isOverageEligibleModel,
  shouldAutoUseCredits,
} from '../billing/billing.js';
import { logBillingEvent, logInvalidChunk } from '../telemetry/loggers.js';

> Provides utility functions for managing and interacting with the CLI sandbox.
```

### `C:/Users/Sasha/gemini-cli\packages\cli\src\utils\sandboxUtils.ts`
```typescript
/**
 * @license
 * Copyright 2025 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import os from 'node:os';
import fs from 'node:fs';
import { readFile } from 'node:fs/promises';
import { quote } from 'shell-quote';
import { debugLogger, GEMINI_DIR } from '@google/gemini-cli-core';

export const LOCAL_DEV_SANDBOX_IMAGE_NAME = 'gemini-cli-sandbox';
export const SANDBOX_NETWORK_NAME = 'gemini-cli-sandbox';
export const SANDBOX_PROXY_NAME = 'gemini-cli-sandbox-proxy';
export const BUILTIN_SEATBELT_PROFILES = [
  'permissive-open',
  'permissive-proxied',
  'restrictive-open',
  'restrictive-proxied',
  'strict-open',
  'strict-proxied',
];

export function getContainerPath(hostPath: string): string {
  if (os.platform() !== 'win32') {
    return hostPath;
  }

  const withForwardSlashes = hostPath.replace(/\\/g, '/');
  const match = withForwardSlashes.match(/^([A-Z]):\/(.*)/i);
  if (match) {
    return `/${match[1].toLowerCase()}/${match[2]}`;
  }
  return withForwardSlashes;
}

export async function shouldUseCurrentUserInSandbox(): Promise<boolean> {
  const envVar = process.env['SANDBOX_SET_UID_GID']?.toLowerCase().trim();

  if (envVar === '1' || envVar === 'true') {
    return true;
  }
  if (envVar === '0' || envVar === 'false') {
    return false;
  }

  // If environment variable is not explicitly set, check for Debian/Ubuntu Linux
  if (os.platform() === 'linux') {
    try {

```


---
_Token estimate: 7314 / 12000_