=== PROJECT SUMMARY ===
Language: Lua
Mixed codebase: Yes
Framework: Unknown
Architectural Pattern: General Project
Entry Point: C:/Users/Sasha/neovim\src\nvim\eval.lua
Total Files: 1312


=== KEY FILES ===


```
--- C:/Users/Sasha/neovim\src\nvim\eval.lua ---
-- File containing table with all functions.
--
-- Keys:
--
--- @class vim.EvalFn
--- @field name? string
--- @field args? integer|integer[] Number of arguments, list with maximum and minimum number of arguments
---       or list with a minimum number of arguments only. Defaults to zero
---       arguments.
--- @field base? integer For methods: the argument to use as the base argument (1-indexed):
---       base->method()
---       Defaults to BASE_NONE (function cannot be used as a method).
--- @field func? string Name of the C function which implements the Vimscript function. Defaults to
---       `f_{funcname}`.
--- @field float_func? string
--- @field fast? boolean Function can run in |api-fast| events. Defaults to false.
--- @field deprecated? true
--- @field returns? string|false
--- @field returns_desc? string
--- @field generics? string[] Used to write `---@generic` annotations over a function.
--- @field signature? string
--- @field desc? string
--- @field params [string, string, string][]
--- @field notes? string[]
--- @field see? string[]
--- @field lua? false Do not render type information
--- @field tags? string[] Extra tags
--- @field data? string Used by gen_eval.lua

-- Usable with the base key: use the last function argument as the method base.
-- Value is from funcs.h file. "BASE_" prefix is omitted.
-- local LAST = "BASE_LAST" (currently unused after port of v8.2.1168)

local M = {}

local VARARGS = { { '...', 'any' } }

--- @type table<string,vim.EvalFn>
M.funcs = {
  abs = {
    args = 1,
    base = 1,
    desc = [=[
      Return the absolute value of {expr}.  When {expr} evaluates to
      a |Float| abs() returns a |Float|.  When {expr} can be
      converted to a |Number| abs() returns a |Number|.  Otherwise
      abs() gives an error message and returns -1.
      Examples: >vim
      	echo abs(1.456)
      <	1.456  >vim


```
--- C:/Users/Sasha/neovim\src\nvim\lua\api_wrappers.c ---
#include <lauxlib.h>  // IWYU pragma: keep
#include <lua.h>  // IWYU pragma: keep
#include <lualib.h>  // IWYU pragma: keep

#include "nvim/api/private/defs.h"  // IWYU pragma: keep
#include "nvim/api/private/dispatch.h"  // IWYU pragma: keep
#include "nvim/api/private/helpers.h"  // IWYU pragma: keep
#include "nvim/errors.h"  // IWYU pragma: keep
#include "nvim/ex_docmd.h"  // IWYU pragma: keep
#include "nvim/ex_getln.h"  // IWYU pragma: keep
#include "nvim/func_attr.h"  // IWYU pragma: keep
#include "nvim/globals.h"  // IWYU pragma: keep
#include "nvim/lua/converter.h"  // IWYU pragma: keep
#include "nvim/lua/executor.h"  // IWYU pragma: keep
#include "nvim/memory.h"  // IWYU pragma: keep

#include "lua_api_c_bindings.generated.h"  // IWYU pragma: keep


```
--- C:/Users/Sasha/neovim\src\nvim\main.h ---
#pragma once

#include <stdbool.h>

#include "nvim/types_defs.h"

// Maximum number of commands from + or -c arguments.
#define MAX_ARG_CMDS 10

extern Loop main_loop;

// Struct for various parameters passed between main() and other functions.
typedef struct {
  int argc;
  char **argv;

  char *use_vimrc;                      // vimrc from -u argument
  bool clean;                           // --clean argument

  int n_commands;                       // no. of commands from + or -c
  char *commands[MAX_ARG_CMDS];         // commands from + or -c arg
  char cmds_tofree[MAX_ARG_CMDS];       // commands that need free()
  int n_pre_commands;                   // no. of commands from --cmd
  char *pre_commands[MAX_ARG_CMDS];     // commands from --cmd argument
  char *luaf;                           // Lua script filename from "-l"
  int lua_arg0;                         // Lua script args start index.

  int edit_type;                        // type of editing to do
  char *tagname;                        // tag from -t argument
  char *use_ef;                         // 'errorfile' from -q argument

  bool input_istext;                    // stdin is text, not executable (-E/-Es)

  int no_swap_file;                     // "-n" argument used
  int use_debug_break_level;
  int window_count;                     // number of windows to use
  int window_layout;                    // 0, WIN_HOR, WIN_VER or WIN_TABS

  int diff_mode;                        // start with 'diff' set

  char *listen_addr;                    // --listen {address}
  int remote;                           // --remote-[subcmd] {file1} {file2}
  char *server_addr;                    // --server {address}
  char *scriptin;                       // -s {filename}
  char *scriptout;                      // -w/-W {filename}
  bool scriptout_append;                // append (-w) instead of overwrite (-W)
  bool had_stdin_file;                  // explicit - as a file to edit
} mparm_T;

#if defined(MSWIN) && !defined(ENABLE_ASAN_UBSAN)


```
--- C:/Users/Sasha/neovim\src\nvim\main.c ---
// Make sure extern symbols are exported on Windows
#ifdef WIN32
# define EXTERN __declspec(dllexport)
#else
# define EXTERN
#endif
#include <assert.h>
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef ENABLE_ASAN_UBSAN
# include <sanitizer/asan_interface.h>
# ifndef MSWIN
#  include <sanitizer/ubsan_interface.h>
# endif
#endif

#include "auto/config.h"  // IWYU pragma: keep
#include "klib/kvec.h"
#include "nvim/api/extmark.h"
#include "nvim/api/private/defs.h"
#include "nvim/api/private/helpers.h"
#include "nvim/api/ui.h"
#include "nvim/arglist.h"
#include "nvim/ascii_defs.h"
#include "nvim/autocmd.h"
#include "nvim/autocmd_defs.h"
#include "nvim/buffer.h"
#include "nvim/buffer_defs.h"
#include "nvim/channel.h"
#include "nvim/channel_defs.h"
#include "nvim/decoration.h"
#include "nvim/decoration_provider.h"
#include "nvim/diff.h"
#include "nvim/drawline.h"
#include "nvim/drawscreen.h"
#include "nvim/errors.h"
#include "nvim/eval.h"
#include "nvim/eval/typval.h"
#include "nvim/eval/typval_defs.h"
#include "nvim/eval/userfunc.h"
#include "nvim/eval/vars.h"
#include "nvim/event/loop.h"
#include "nvim/event/multiqueue.h"
#include "nvim/event/proc.h"
#include "nvim/event/socket.h"


```
--- C:/Users/Sasha/neovim\src\mpack\mpack_core.c ---
#include <string.h>

#include "mpack_core.h"

#define UNUSED(p) (void)p;
#define ADVANCE(buf, buflen) ((*buflen)--, (unsigned char)*((*buf)++))
#define TLEN(val, range_start) ((mpack_uint32_t)(1 << (val - range_start)))
#ifndef MIN
# define MIN(X, Y) ((X) < (Y) ? (X) : (Y))
#endif

static int mpack_rpending(const char **b, size_t *nl, mpack_tokbuf_t *tb);
static int mpack_rvalue(mpack_token_type_t t, mpack_uint32_t l,
    const char **b, size_t *bl, mpack_token_t *tok);
static int mpack_rblob(mpack_token_type_t t, mpack_uint32_t l,
    const char **b, size_t *bl, mpack_token_t *tok);
static int mpack_wtoken(const mpack_token_t *tok, char **b, size_t *bl);
static int mpack_wpending(char **b, size_t *bl, mpack_tokbuf_t *tb);
static int mpack_wpint(char **b, size_t *bl, mpack_value_t v);
static int mpack_wnint(char **b, size_t *bl, mpack_value_t v);
static int mpack_wfloat(char **b, size_t *bl, const mpack_token_t *v);
static int mpack_wstr(char **buf, size_t *buflen, mpack_uint32_t len);
static int mpack_wbin(char **buf, size_t *buflen, mpack_uint32_t len);
static int mpack_wext(char **buf, size_t *buflen, int type,
    mpack_uint32_t len);
static int mpack_warray(char **buf, size_t *buflen, mpack_uint32_t len);
static int mpack_wmap(char **buf, size_t *buflen, mpack_uint32_t len);
static int mpack_w1(char **b, size_t *bl, mpack_uint32_t v);
static int mpack_w2(char **b, size_t *bl, mpack_uint32_t v);
static int mpack_w4(char **b, size_t *bl, mpack_uint32_t v);
static mpack_value_t mpack_byte(unsigned char b);
static int mpack_value(mpack_token_type_t t, mpack_uint32_t l,
    mpack_value_t v, mpack_token_t *tok);
static int mpack_blob(mpack_token_type_t t, mpack_uint32_t l, int et,
    mpack_token_t *tok);

MPACK_API void mpack_tokbuf_init(mpack_tokbuf_t *tokbuf)
{
  tokbuf->ppos = 0;
  tokbuf->plen = 0;
  tokbuf->passthrough = 0;
}

MPACK_API int mpack_read(mpack_tokbuf_t *tokbuf, const char **buf,
    size_t *buflen, mpack_token_t *tok)
{
  int status;
  size_t initial_ppos, ptrlen, advanced;
  const char *ptr, *ptr_save;
  assert(*buf);


```
--- C:/Users/Sasha/neovim\src\mpack\mpack_core.h ---
#ifndef MPACK_CORE_H
#define MPACK_CORE_H

#ifndef MPACK_API
# define MPACK_API extern
#endif

#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __GNUC__
# define FPURE __attribute__((const))
# define FNONULL __attribute__((nonnull))
# define FNONULL_ARG(x) __attribute__((nonnull x))
# define FUNUSED __attribute__((unused))
#else
# define FPURE
# define FNONULL
# define FNONULL_ARG(x)
# define FUNUSED
#endif

#if UINT_MAX == 0xffffffff
typedef int mpack_sint32_t;
typedef unsigned int mpack_uint32_t;
#elif ULONG_MAX == 0xffffffff
typedef long mpack_sint32_t;
typedef unsigned long mpack_uint32_t;
#else
# error "can't find unsigned 32-bit integer type"
#endif

typedef struct mpack_value_s {
  mpack_uint32_t lo, hi;
} mpack_value_t;


enum {
  MPACK_OK = 0,
  MPACK_EOF = 1,
  MPACK_ERROR = 2
};

#define MPACK_MAX_TOKEN_LEN 9  /* 64-bit ints/floats plus type code */

typedef enum {
  MPACK_TOKEN_NIL       = 1,
  MPACK_TOKEN_BOOLEAN   = 2,


```
--- C:/Users/Sasha/neovim\src\nvim\mapping.c ---
// mapping.c: Code for mappings and abbreviations.

#include <assert.h>
#include <lauxlib.h>
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "klib/kvec.h"
#include "nvim/api/keysets_defs.h"
#include "nvim/api/private/converter.h"
#include "nvim/api/private/defs.h"
#include "nvim/api/private/dispatch.h"
#include "nvim/api/private/helpers.h"
#include "nvim/ascii_defs.h"
#include "nvim/buffer_defs.h"
#include "nvim/charset.h"
#include "nvim/cmdexpand.h"
#include "nvim/cmdexpand_defs.h"
#include "nvim/errors.h"
#include "nvim/eval.h"
#include "nvim/eval/typval.h"
#include "nvim/eval/typval_defs.h"
#include "nvim/eval/userfunc.h"
#include "nvim/eval/vars.h"
#include "nvim/ex_cmds_defs.h"
#include "nvim/ex_session.h"
#include "nvim/fuzzy.h"
#include "nvim/garray.h"
#include "nvim/garray_defs.h"
#include "nvim/getchar.h"
#include "nvim/getchar_defs.h"
#include "nvim/gettext_defs.h"
#include "nvim/globals.h"
#include "nvim/highlight_defs.h"
#include "nvim/keycodes.h"
#include "nvim/lua/executor.h"
#include "nvim/macros_defs.h"
#include "nvim/mapping.h"
#include "nvim/mapping_defs.h"
#include "nvim/mbyte.h"
#include "nvim/mbyte_defs.h"
#include "nvim/memory.h"
#include "nvim/memory_defs.h"
#include "nvim/message.h"
#include "nvim/option_defs.h"
#include "nvim/option_vars.h"


```
--- C:/Users/Sasha/neovim\src\nvim\mapping.h ---
#pragma once

#include <stdint.h>  // IWYU pragma: keep
#include <stdio.h>  // IWYU pragma: keep

#include "nvim/api/keysets_defs.h"  // IWYU pragma: keep
#include "nvim/api/private/defs.h"  // IWYU pragma: keep
#include "nvim/cmdexpand_defs.h"  // IWYU pragma: keep
#include "nvim/eval/typval_defs.h"  // IWYU pragma: keep
#include "nvim/ex_cmds_defs.h"  // IWYU pragma: keep
#include "nvim/mapping_defs.h"  // IWYU pragma: keep
#include "nvim/option_defs.h"  // IWYU pragma: keep
#include "nvim/regexp_defs.h"  // IWYU pragma: keep
#include "nvim/types_defs.h"  // IWYU pragma: keep

#include "mapping.h.generated.h"

/// Used for the first argument of do_map()
enum {
  MAPTYPE_MAP       = 0,
  MAPTYPE_UNMAP     = 1,
  MAPTYPE_NOREMAP   = 2,
  MAPTYPE_UNMAP_LHS = 3,
};

/// Adjust chars in a language according to 'langmap' option.
/// NOTE that there is no noticeable overhead if 'langmap' is not set.
/// When set the overhead for characters < 256 is small.
/// Don't apply 'langmap' if the character comes from the Stuff buffer or from a
/// mapping and the langnoremap option was set.
/// The do-while is just to ignore a ';' after the macro.
#define LANGMAP_ADJUST(c, condition) \
  do { \
    if (*p_langmap \
        && (condition) \
        && (p_lrm || (vgetc_busy ? typebuf_maplen() == 0 : KeyTyped)) \
        && !KeyStuffed \
        && (c) >= 0) \
    { \
      if ((c) < 256) \
      c = langmap_mapchar[c]; \
      else \
      c = langmap_adjust_mb(c); \
    } \
  } while (0)


```
--- C:/Users/Sasha/neovim\src\nvim\mapping_defs.h ---
#pragma once

#include <stdbool.h>

#include "nvim/eval/typval_defs.h"

enum { MAXMAPLEN = 50, };  ///< Maximum length of key sequence to be mapped.

/// Structure used for mappings and abbreviations.
typedef struct mapblock mapblock_T;
struct mapblock {
  mapblock_T *m_next;       ///< next mapblock in list
  mapblock_T *m_alt;        ///< pointer to mapblock of the same mapping
                            ///< with an alternative form of m_keys, or NULL
                            ///< if there is no such mapblock
  char *m_keys;             ///< mapped from, lhs
  char *m_str;              ///< mapped to, rhs
  char *m_orig_str;         ///< rhs as entered by the user
  LuaRef m_luaref;          ///< lua function reference as rhs
  int m_keylen;             ///< strlen(m_keys)
  int m_mode;               ///< valid mode
  int m_simplified;         ///< m_keys was simplified
  int m_noremap;            ///< if non-zero no re-mapping for m_str
  char m_silent;            ///< <silent> used, don't echo commands
  char m_nowait;            ///< <nowait> used
  char m_expr;              ///< <expr> used, m_str is an expression
  sctx_T m_script_ctx;      ///< SCTX where map was defined
  char *m_desc;             ///< description of mapping
  bool m_replace_keycodes;  ///< replace keycodes in result of expression
};


```
--- C:/Users/Sasha/neovim\src\nvim\msgpack_rpc\server.c ---
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <uv.h>

#include "nvim/ascii_defs.h"
#include "nvim/channel.h"
#include "nvim/eval/vars.h"
#include "nvim/event/defs.h"
#include "nvim/event/socket.h"
#include "nvim/garray.h"
#include "nvim/garray_defs.h"
#include "nvim/globals.h"
#include "nvim/log.h"
#include "nvim/main.h"
#include "nvim/memory.h"
#include "nvim/msgpack_rpc/server.h"
#include "nvim/os/os.h"
#include "nvim/os/os_defs.h"
#include "nvim/os/stdpaths_defs.h"
#include "nvim/path.h"
#include "nvim/types_defs.h"

#define MAX_CONNECTIONS 32
#define ENV_LISTEN "NVIM_LISTEN_ADDRESS"  // deprecated

static garray_T watchers = GA_EMPTY_INIT_VALUE;

#include "msgpack_rpc/server.c.generated.h"

/// Initializes resources, handles `--listen`, starts the primary server at v:servername.
///
/// @returns true on success, false on fatal error (message stored in IObuff)
bool server_init(const char *listen_addr)
{
  bool ok = true;
  bool must_free = false;
  TriState user_arg = kTrue;  // User-provided --listen arg.
  ga_init(&watchers, sizeof(SocketWatcher *), 1);

  // $NVIM_LISTEN_ADDRESS (deprecated)
  if (!listen_addr || listen_addr[0] == '\0') {
    if (os_env_exists(ENV_LISTEN, true)) {
      user_arg = kFalse;  // User-provided env var.
      listen_addr = os_getenv(ENV_LISTEN);
    } else {
      user_arg = kNone;  // Autogenerated server address.
      listen_addr = server_address_new(NULL);
    }


```
--- C:/Users/Sasha/neovim\src\clint.lua ---
#!/usr/bin/env nvim -l
---@diagnostic disable: no-unknown

-- Lints C files in the Neovim source tree.
-- Based on Google "cpplint", modified for Neovim.
--
-- Test coverage: `test/functional/script/clint_spec.lua`
--
-- This can get very confused by /* and // inside strings! We do a small hack,
-- which is to ignore //'s with "'s after them on the same line, but it is far
-- from perfect (in either direction).

local vim = vim

-- Error categories used for filtering
local ERROR_CATEGORIES = {
  'build/endif_comment',
  'build/header_guard',
  'build/include_defs',
  'build/defs_header',
  'build/printf_format',
  'build/storage_class',
  'build/init_macro',
  'readability/bool',
  'readability/multiline_comment',
  -- Dropped 'readability/multiline_string' detection because it is too buggy, and uncommon.
  -- 'readability/multiline_string',
  'readability/nul',
  'readability/utf8',
  'readability/increment',
  'runtime/arrays',
  'runtime/int',
  'runtime/memset',
  'runtime/printf',
  'runtime/printf_format',
  'runtime/threadsafe_fn',
  'runtime/deprecated',
  'whitespace/indent',
  'whitespace/operators',
  'whitespace/cast',
}

-- Default filters (empty by default)
local DEFAULT_FILTERS = {}

-- Assembly state constants
local NO_ASM = 0 -- Outside of inline assembly block
local INSIDE_ASM = 1 -- Inside inline assembly block
local END_ASM = 2 -- Last line of inline assembly block
local BLOCK_ASM = 3 -- The whole block is an inline assembly block


```
--- C:/Users/Sasha/neovim\src\nvim\msgpack_rpc\server.h ---
#pragma once

#include <stdbool.h>
#include <stddef.h>  // IWYU pragma: keep

#include "msgpack_rpc/server.h.generated.h"


```
--- C:/Users/Sasha/neovim\src\nvim\clipboard.c ---
// clipboard.c: Functions to handle the clipboard

#include <assert.h>

#include "nvim/api/private/helpers.h"
#include "nvim/ascii_defs.h"
#include "nvim/clipboard.h"
#include "nvim/eval.h"
#include "nvim/eval/typval.h"
#include "nvim/option_vars.h"
#include "nvim/register.h"

#include "clipboard.c.generated.h"

// for behavior between start_batch_changes() and end_batch_changes())
static int batch_change_count = 0;           // inside a script
static bool clipboard_delay_update = false;  // delay clipboard update
static bool clipboard_needs_update = false;  // clipboard was updated
static bool clipboard_didwarn = false;

/// Determine if register `*name` should be used as a clipboard.
/// In an unnamed operation, `*name` is `NUL` and will be adjusted to */+ if
/// `clipboard=unnamed[plus]` is set.
///
/// @param name The name of register, or `NUL` if unnamed.
/// @param quiet Suppress error messages
/// @param writing if we're setting the contents of the clipboard
///
/// @returns the yankreg that should be written into, or `NULL`
/// if the register isn't a clipboard or provider isn't available.
yankreg_T *adjust_clipboard_name(int *name, bool quiet, bool writing)
{
#define MSG_NO_CLIP "clipboard: No provider. " \
  "Try \":checkhealth\" or \":h clipboard\"."

  yankreg_T *target = NULL;
  bool explicit_cb_reg = (*name == '*' || *name == '+');
  bool implicit_cb_reg = (*name == NUL) && (cb_flags & (kOptCbFlagUnnamed | kOptCbFlagUnnamedplus));
  if (!explicit_cb_reg && !implicit_cb_reg) {
    goto end;
  }

  if (!eval_has_provider("clipboard", false)) {
    if (batch_change_count <= 1 && !quiet
        && (!clipboard_didwarn || (explicit_cb_reg && !redirecting()))) {
      clipboard_didwarn = true;
      // Do NOT error (emsg()) here--if it interrupts :redir we get into
      // a weird state, stuck in "redirect mode".
      msg(MSG_NO_CLIP, 0);
    }


```
--- C:/Users/Sasha/neovim\src\nvim\clipboard.h ---
#pragma once

#include <stdbool.h>

#include "nvim/register_defs.h"

#include "clipboard.h.generated.h"


```
--- C:/Users/Sasha/neovim\src\nvim\ui_client.c ---
/// Nvim's own UI client, which attaches to a child or remote Nvim server.

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

#include "nvim/api/keysets_defs.h"
#include "nvim/api/private/defs.h"
#include "nvim/api/private/helpers.h"
#include "nvim/channel.h"
#include "nvim/channel_defs.h"
#include "nvim/eval/typval_defs.h"
#include "nvim/event/multiqueue.h"
#include "nvim/event/socket.h"
#include "nvim/globals.h"
#include "nvim/highlight.h"
#include "nvim/highlight_defs.h"
#include "nvim/log.h"
#include "nvim/main.h"
#include "nvim/memory.h"
#include "nvim/memory_defs.h"
#include "nvim/msgpack_rpc/channel.h"
#include "nvim/msgpack_rpc/channel_defs.h"
#include "nvim/os/os.h"
#include "nvim/profile.h"
#include "nvim/tui/tui.h"
#include "nvim/tui/tui_defs.h"
#include "nvim/ui.h"
#include "nvim/ui_client.h"
#include "nvim/ui_defs.h"

#ifdef MSWIN
# include "nvim/os/os_win_console.h"
#endif

static TUIData *tui = NULL;
static int tui_width = 0;
static int tui_height = 0;
static char *tui_term = "";
static bool tui_rgb = false;
static bool ui_client_is_remote = false;

// uncrustify:off
#include "ui_client.c.generated.h"
#include "ui_events_client.generated.h"
// uncrustify:on

uint64_t ui_client_start_server(const char *exepath, size_t argc, char **argv)
{


```
--- C:/Users/Sasha/neovim\src\nvim\ui_client.h ---
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "nvim/grid_defs.h"  // IWYU pragma: keep
#include "nvim/macros_defs.h"
#include "nvim/types_defs.h"
#include "nvim/ui_defs.h"  // IWYU pragma: keep

// Temporary buffer for converting a single grid_line event
EXTERN size_t grid_line_buf_size INIT( = 0);
EXTERN schar_T *grid_line_buf_char INIT( = NULL);
EXTERN sattr_T *grid_line_buf_attr INIT( = NULL);

// Client-side UI channel. Zero during early startup or if not a (--remote-ui) UI client.
EXTERN uint64_t ui_client_channel_id INIT( = 0);

/// `status` argument of the last "error_exit" UI event, or -1 if none has been seen.
/// NOTE: This assumes "error_exit" never has a negative `status` argument.
EXTERN int ui_client_error_exit INIT( = -1);

/// Server exit code.
EXTERN int ui_client_exit_status INIT( = 0);

/// Whether ui client has sent nvim_ui_attach yet
EXTERN bool ui_client_attached INIT( = false);

/// The ui client should forward its stdin to the nvim process
/// by convention, this uses fd=3 (next free number after stdio)
EXTERN bool ui_client_forward_stdin INIT( = false);

#define UI_CLIENT_STDIN_FD 3
// uncrustify:off
# include "ui_client.h.generated.h"
# include "ui_events_client.h.generated.h"
// uncrustify:on


```
--- C:/Users/Sasha/neovim\src\nvim\api\win_config.c ---
#include <assert.h>
#include <stdbool.h>
#include <string.h>

#include "klib/kvec.h"
#include "nvim/api/extmark.h"
#include "nvim/api/keysets_defs.h"
#include "nvim/api/private/defs.h"
#include "nvim/api/private/dispatch.h"
#include "nvim/api/private/helpers.h"
#include "nvim/api/private/validate.h"
#include "nvim/api/win_config.h"
#include "nvim/ascii_defs.h"
#include "nvim/autocmd.h"
#include "nvim/autocmd_defs.h"
#include "nvim/buffer.h"
#include "nvim/buffer_defs.h"
#include "nvim/decoration_defs.h"
#include "nvim/drawscreen.h"
#include "nvim/errors.h"
#include "nvim/eval/window.h"
#include "nvim/ex_cmds_defs.h"
#include "nvim/ex_docmd.h"
#include "nvim/globals.h"
#include "nvim/highlight_group.h"
#include "nvim/macros_defs.h"
#include "nvim/mbyte.h"
#include "nvim/memory.h"
#include "nvim/memory_defs.h"
#include "nvim/move.h"
#include "nvim/option.h"
#include "nvim/option_vars.h"
#include "nvim/pos_defs.h"
#include "nvim/strings.h"
#include "nvim/syntax.h"
#include "nvim/types_defs.h"
#include "nvim/ui.h"
#include "nvim/ui_compositor.h"
#include "nvim/ui_defs.h"
#include "nvim/vim_defs.h"
#include "nvim/window.h"
#include "nvim/winfloat.h"

#include "api/win_config.c.generated.h"

#define HAS_KEY_X(d, key) HAS_KEY(d, win_config, key)

/// Opens a new split window, floating window, or external window.
///
/// - Specify `relative` to create a floating window. Floats are drawn over the split layout,


```
--- C:/Users/Sasha/neovim\src\nvim\api\win_config.h ---
#pragma once

#include <stdint.h>  // IWYU pragma: keep

#include "nvim/api/keysets_defs.h"  // IWYU pragma: keep
#include "nvim/api/private/defs.h"  // IWYU pragma: keep
#include "nvim/buffer_defs.h"  // IWYU pragma: keep

#include "api/win_config.h.generated.h"


```
--- C:/Users/Sasha/neovim\test\functional\core\main_spec.lua ---
local t = require('test.testutil')
local n = require('test.functional.testnvim')()
local Screen = require('test.functional.ui.screen')
local uv = vim.uv

local eq = t.eq
local matches = t.matches
local feed = n.feed
local eval = n.eval
local clear = n.clear
local fn = n.fn
local write_file = t.write_file
local is_os = t.is_os
local skip = t.skip

describe('command-line option', function()
  describe('-s', function()
    local fname = 'Xtest-functional-core-main-s'
    local fname_2 = fname .. '.2'
    local nonexistent_fname = fname .. '.nonexistent'
    local dollar_fname = '$' .. fname

    before_each(function()
      clear()
      os.remove(fname)
      os.remove(dollar_fname)
    end)

    after_each(function()
      os.remove(fname)
      os.remove(dollar_fname)
    end)

    it('treats - as stdin', function()
      eq(nil, uv.fs_stat(fname))
      fn.system({
        n.nvim_prog,
        '-u',
        'NONE',
        '-i',
        'NONE',
        '--headless',
        '--cmd',
        'set noswapfile shortmess+=IFW fileformats=unix',
        '-s',
        '-',
        fname,
      }, { ':call setline(1, "42")', ':wqall!', '' })
      eq(0, eval('v:shell_error'))
      local attrs = uv.fs_stat(fname)


```
--- C:/Users/Sasha/neovim\test\old\testdir\test_clientserver.vim ---
" Tests for the +clientserver feature.

source check.vim
CheckFeature job

if !has('clientserver')
  call assert_fails('call remote_startserver("local")', 'E942:')
endif

CheckFeature clientserver

source shared.vim

func Check_X11_Connection()
  if has('x11')
    CheckEnv DISPLAY
    try
      call remote_send('xxx', '')
    catch
      if v:exception =~ 'E240:'
        throw 'Skipped: no connection to the X server'
      endif
      " ignore other errors
    endtry
  endif
endfunc

func Test_client_server()
  let g:test_is_flaky = 1
  let cmd = GetVimCommand()
  if cmd == ''
    throw 'GetVimCommand() failed'
  endif
  call Check_X11_Connection()

  let name = 'XVIMTEST'
  let cmd .= ' --servername ' . name
  let job = job_start(cmd, {'stoponexit': 'kill', 'out_io': 'null'})
  call WaitForAssert({-> assert_equal("run", job_status(job))})

  " Takes a short while for the server to be active.
  " When using valgrind it takes much longer.
  call WaitForAssert({-> assert_match(name, serverlist())})

  if !has('win32')
    if RunVim([], [], '--serverlist >Xtest_serverlist')
      let lines = readfile('Xtest_serverlist')
      call assert_true(index(lines, 'XVIMTEST') >= 0)
    endif
    call delete('Xtest_serverlist')


```
--- C:/Users/Sasha/neovim\src\coverity-model.c ---
// Coverity Scan model
//
// This is a modeling file for Coverity Scan. Modeling helps to avoid false
// positives.
//
// - A model file can't import any header files.
// - Therefore only some built-in primitives like int, char and void are
//   available but not wchar_t, NULL etc.
// - Modeling doesn't need full structs and typedefs. Rudimentary structs
//   and similar types are sufficient.
// - An uninitialized local pointer is not an error. It signifies that the
//   variable could be either NULL or have some data.
//
// Coverity Scan doesn't pick up modifications automatically. The model file
// must be uploaded by an admin in the analysis settings of
// http://scan.coverity.com/projects/neovim-neovim
//

// Issue 105985
//
// Teach coverity that uv_pipe_open saves fd on success (0 return value)
// and doesn't save it on failure (return value != 0).

struct uv_pipe_s {
  int something;
};

int uv_pipe_open(struct uv_pipe_s *handle, int fd)
{
  int result;
  if (result == 0) {
    __coverity_escape__(fd);
  }
  return result;
}

// Hint Coverity that adding item to d avoids losing track
// of the memory allocated for item.
typedef struct {} dictitem_T;
typedef struct {} dict_T;
int tv_dict_add(dict_T *const d, dictitem_T *const item)
{
  __coverity_escape__(item);
}

void *malloc(size_t size)
{
  int has_mem;
  if (has_mem)
    return __coverity_alloc__(size);


```
--- C:/Users/Sasha/neovim\test\functional\core\server_spec.lua ---
local t = require('test.testutil')
local n = require('test.functional.testnvim')()

local eq, neq, eval = t.eq, t.neq, n.eval
local clear, fn, api = n.clear, n.fn, n.api
local matches = t.matches
local pcall_err = t.pcall_err
local check_close = n.check_close
local mkdir = t.mkdir
local rmdir = n.rmdir
local is_os = t.is_os

local testlog = 'Xtest-server-log'

local function clear_serverlist()
  for _, server in pairs(fn.serverlist()) do
    fn.serverstop(server)
  end
end

after_each(function()
  check_close()
  os.remove(testlog)
end)

before_each(function()
  os.remove(testlog)
end)

describe('server', function()
  it('serverstart() stores sockets in $XDG_RUNTIME_DIR', function()
    local dir = 'Xtest_xdg_run'
    mkdir(dir)
    finally(function()
      rmdir(dir)
    end)
    clear({ env = { XDG_RUNTIME_DIR = dir } })
    matches(dir, fn.stdpath('run'))
    if not is_os('win') then
      matches(dir, fn.serverstart())
    end
  end)

  it('broken $XDG_RUNTIME_DIR is not fatal #30282', function()
    clear {
      args_rm = { '--listen' },
      env = { NVIM_LOG_FILE = testlog, XDG_RUNTIME_DIR = '/non-existent-dir/subdir//' },
    }

    if is_os('win') then


```
--- C:/Users/Sasha/neovim\src\nvim\option.h ---
#pragma once

#include <stdio.h>  // IWYU pragma: keep

#include "nvim/api/private/defs.h"  // IWYU pragma: keep
#include "nvim/api/private/helpers.h"
#include "nvim/cmdexpand_defs.h"  // IWYU pragma: keep
#include "nvim/eval/typval_defs.h"  // IWYU pragma: keep
#include "nvim/ex_cmds_defs.h"  // IWYU pragma: keep
#include "nvim/macros_defs.h"
#include "nvim/option_defs.h"  // IWYU pragma: keep
#include "nvim/types_defs.h"  // IWYU pragma: keep

/// flags for buf_copy_options()
enum {
  BCO_ENTER  = 1,  ///< going to enter the buffer
  BCO_ALWAYS = 2,  ///< always copy the options
  BCO_NOHELP = 4,  ///< don't touch the help related options
};

/// Flags for option-setting functions
///
/// When OPT_GLOBAL and OPT_LOCAL are both missing, set both local and global
/// values, get local value.
typedef enum {
  OPT_GLOBAL    = 0x01,  ///< Use global value.
  OPT_LOCAL     = 0x02,  ///< Use local value.
  OPT_MODELINE  = 0x04,  ///< Option in modeline.
  OPT_WINONLY   = 0x08,  ///< Only set window-local options.
  OPT_NOWIN     = 0x10,  ///< Don’t set window-local options.
  OPT_ONECOLUMN = 0x20,  ///< list options one per line
  OPT_NO_REDRAW = 0x40,  ///< ignore redraw flags on option
  OPT_SKIPRTP   = 0x80,  ///< "skiprtp" in 'sessionoptions'
} OptionSetFlags;

/// Get name of OptValType as a string.
static inline const char *optval_type_get_name(const OptValType type)
{
  switch (type) {
  case kOptValTypeNil:
    return "nil";
  case kOptValTypeBoolean:
    return "boolean";
  case kOptValTypeNumber:
    return "number";
  case kOptValTypeString:
    return "string";
  }
  UNREACHABLE;
}


```
--- C:/Users/Sasha/neovim\src\nvim\options.lua ---
-- vim: tw=78

--- @class vim.option_meta
--- @field full_name string
--- @field desc? string
--- @field abbreviation? string
--- @field alias? string|string[]
--- @field short_desc? string|fun(): string
--- @field varname? string
--- @field flags_varname? string
--- @field type vim.option_type
--- @field immutable? boolean
--- @field list? 'comma'|'onecomma'|'commacolon'|'onecommacolon'|'flags'|'flagscomma'
--- @field scope vim.option_scope[]
--- @field deny_duplicates? boolean
--- @field enable_if? string
--- @field defaults? vim.option_defaults|vim.option_value|fun(): string
--- @field values? vim.option_valid_values
--- @field flags? true|table<string,integer>
--- @field secure? true
--- @field noglob? true
--- @field normal_fname_chars? true
--- @field pri_mkrc? true
--- @field deny_in_modelines? true
--- @field normal_dname_chars? true
--- @field modelineexpr? true
--- @field func? true
--- @field expand? string|true
--- @field nodefault? true
--- @field no_mkrc? true
--- @field alloced? true
--- @field redraw? vim.option_redraw[]
---
--- If not provided and `values` is present, then is set to 'did_set_str_generic'
--- @field cb? string
---
--- If not provided and `values` is present, then is set to 'expand_set_str_generic'
--- @field expand_cb? string
--- @field tags? string[]

--- @class vim.option_defaults
--- @field condition? string
---    string: #ifdef string
---    !string: #ifndef string
--- @field if_true vim.option_value|fun(): string
--- @field if_false? vim.option_value
--- @field doc? string Default to show in options.txt
--- @field meta? string Default to use in Lua meta files

--- @alias vim.option_scope 'global'|'buf'|'win'


```
--- C:/Users/Sasha/neovim\src\nvim\option_defs.h ---
#pragma once

#include <stdbool.h>
#include <stddef.h>

#include "nvim/api/private/defs.h"
#include "nvim/cmdexpand_defs.h"
#include "nvim/regexp_defs.h"

#include "options_enum.generated.h"

/// Option flags.
typedef enum {
  kOptFlagExpand    = 1 << 0,  ///< Environment expansion.
                               ///< NOTE: kOptFlagExpand can never be used for local or hidden options.
  kOptFlagNoDefExp  = 1 << 1,  ///< Don't expand default value.
  kOptFlagNoDefault = 1 << 2,  ///< Don't set to default value.
  kOptFlagWasSet    = 1 << 3,  ///< Option has been set/reset.
  kOptFlagNoMkrc    = 1 << 4,  ///< Don't include in :mkvimrc output.
  kOptFlagUIOption  = 1 << 5,  ///< Send option to remote UI.
  kOptFlagRedrTabl  = 1 << 6,  ///< Redraw tabline.
  kOptFlagRedrStat  = 1 << 7,  ///< Redraw status lines.
  kOptFlagRedrWin   = 1 << 8,  ///< Redraw current window and recompute text.
  kOptFlagRedrBuf   = 1 << 9,  ///< Redraw current buffer and recompute text.
  kOptFlagRedrAll   = kOptFlagRedrBuf | kOptFlagRedrWin,  ///< Redraw all windows and recompute text.
  kOptFlagRedrClear = kOptFlagRedrAll | kOptFlagRedrStat,  ///< Clear and redraw all and recompute text.
  kOptFlagComma     = 1 << 10,  ///< Comma-separated list.
  kOptFlagOneComma  = (1 << 11) | kOptFlagComma,  ///< Comma-separated list that cannot have two consecutive commas.
  kOptFlagNoDup     = 1 << 12,  ///< Don't allow duplicate strings.
  kOptFlagFlagList  = 1 << 13,  ///< List of single-char flags.
  kOptFlagSecure    = 1 << 14,  ///< Cannot change in modeline or secure mode.
  kOptFlagGettext   = 1 << 15,  ///< Expand default value with _().
  kOptFlagNoGlob    = 1 << 16,  ///< Do not use local value for global vimrc.
  kOptFlagNFname    = 1 << 17,  ///< Only normal file name chars allowed.
  kOptFlagInsecure  = 1 << 18,  ///< Option was set from a modeline.
  kOptFlagPriMkrc   = 1 << 19,  ///< Priority for :mkvimrc (setting option has side effects).
  kOptFlagNoML      = 1 << 20,  ///< Not allowed in modeline.
  kOptFlagCurswant  = 1 << 21,  ///< Update curswant required; not needed when there is a redraw flag.
  kOptFlagNDname    = 1 << 22,  ///< Only normal directory name chars allowed.
  kOptFlagHLOnly    = 1 << 23,  ///< Option only changes highlight, not text.
  kOptFlagMLE       = 1 << 24,  ///< Under control of 'modelineexpr'.
  kOptFlagFunc      = 1 << 25,  ///< Accept a function reference or a lambda.
  kOptFlagColon     = 1 << 26,  ///< Values use colons to create sublists.
} OptFlags;

/// Option value type.
/// These types are also used as type flags by using the type value as an index for the type_flags
/// bit field (@see option_has_type()).
typedef enum {
  kOptValTypeNil = -1,  // Make sure Nil can't be bitshifted and used as an option type flag.


```
--- C:/Users/Sasha/neovim\src\nvim\runtime_defs.h ---
#pragma once

#include <stdbool.h>

#include "nvim/autocmd_defs.h"

typedef enum {
  ETYPE_TOP,       ///< toplevel
  ETYPE_SCRIPT,    ///< sourcing script, use es_info.sctx
  ETYPE_UFUNC,     ///< user function, use es_info.ufunc
  ETYPE_AUCMD,     ///< autocomand, use es_info.aucmd
  ETYPE_MODELINE,  ///< modeline, use es_info.sctx
  ETYPE_EXCEPT,    ///< exception, use es_info.exception
  ETYPE_ARGS,      ///< command line argument
  ETYPE_ENV,       ///< environment variable
  ETYPE_INTERNAL,  ///< internal operation
  ETYPE_SPELL,     ///< loading spell file
} etype_T;

/// Entry in the execution stack "exestack".
typedef struct {
  linenr_T es_lnum;     ///< replaces "sourcing_lnum"
  char *es_name;        ///< replaces "sourcing_name"
  etype_T es_type;
  union {
    sctx_T *sctx;       ///< script and modeline info
    ufunc_T *ufunc;     ///< function info
    AutoPatCmd *aucmd;  ///< autocommand info
    except_T *except;   ///< exception info
  } es_info;
} estack_T;

/// Argument for estack_sfile().
typedef enum {
  ESTACK_NONE,
  ESTACK_SFILE,
  ESTACK_STACK,
  ESTACK_SCRIPT,
} estack_arg_T;

/// Holds the hashtab with variables local to each sourced script.
/// Each item holds a variable (nameless) that points to the dict_T.
typedef struct {
  ScopeDictDictItem sv_var;
  dict_T sv_dict;
} scriptvar_T;

typedef struct {
  scriptvar_T *sn_vars;         ///< stores s: variables for this script


```
--- C:/Users/Sasha/neovim\test\functional\autocmd\searchwrapped_spec.lua ---
local t = require('test.testutil')
local n = require('test.functional.testnvim')()

local clear = n.clear
local command = n.command
local api = n.api
local eq = t.eq
local eval = n.eval
local feed = n.feed

describe('autocmd SearchWrapped', function()
  before_each(function()
    clear()
    command('set ignorecase')
    command('let g:test = 0')
    command('autocmd! SearchWrapped * let g:test += 1')
    api.nvim_buf_set_lines(0, 0, 1, false, {
      'The quick brown fox',
      'jumps over the lazy dog',
    })
  end)

  it('gets triggered when search wraps the end', function()
    feed('/the<Return>')
    eq(0, eval('g:test'))

    feed('n')
    eq(1, eval('g:test'))

    feed('nn')
    eq(2, eval('g:test'))
  end)

  it('gets triggered when search wraps in reverse order', function()
    feed('/the<Return>')
    eq(0, eval('g:test'))

    feed('NN')
    eq(1, eval('g:test'))

    feed('NN')
    eq(2, eval('g:test'))
  end)

  it('does not get triggered on failed searches', function()
    feed('/blargh<Return>')
    eq(0, eval('g:test'))

    feed('NN')
    eq(0, eval('g:test'))

[Token budget reached — use Deep Dive for remaining files]

```

=== Token estimate: 10729 / 12000 ===