# WARP MASQUE → Proton VPN Free → Gaijin

`build_vpn_in_vpn.sh` adds a **free Proton VPN WireGuard hop** in front of your
existing **Cloudflare WARP MASQUE** profile.

The goal is to stop Gaijin from seeing **AS13335** as the last-mile egress:

```text
War Thunder UDP
  -> Proton VPN Free (WireGuard)
  -> WARP MASQUE / Cloudflare
  -> Proton egress (non-AS13335)
  -> Gaijin
```

This is an experiment. It is not guaranteed to work: Proton's free servers can be
slow, and Gaijin may also rate-limit Proton.

## What this script does **not** do

- It does **not** contain WARP MASQUE private keys.
- It does **not** ship a pre-made WARP profile.
- Every user must have their own WARP MASQUE profile in Clash Verge Rev
  (generated with `usque` / `warp-masque-actions`).
- It does **not** create a Proton account.

The script only:

1. generates a Proton free WireGuard config with
   [`protonvpn-wg-confgen`](https://github.com/hatemosphere/protonvpn-wg-confgen);
2. creates a Clash Verge **Merge** snippet that adds a `Proton-Free` proxy,
   a `🎮 WT-VPN` group, and rules for UDP 20010/20011.

## Requirements

- macOS or Linux (Windows: use WSL/Git Bash);
- `python3`, `curl`, `tar`;
- Clash Verge Rev with your own WARP MASQUE profile already imported and working;
- a free [Proton VPN](https://protonvpn.com/free-vpn) account.

### One-line run (after the repo is pushed)

```bash
curl -fsSL https://raw.githubusercontent.com/LG-leo/WarThunder_Issue/main/build_vpn_in_vpn.sh | bash
```

The script detects that it came from stdin and stores generated files in
`~/WT_CF` by default. Prompts are read from `/dev/tty`, so the user can still
type the Proton username/password.

Safer alternative (review before running):

```bash
curl -fsSL https://raw.githubusercontent.com/LG-leo/WarThunder_Issue/main/build_vpn_in_vpn.sh \
  -o build_vpn_in_vpn.sh
less build_vpn_in_vpn.sh
bash build_vpn_in_vpn.sh
```

If `raw.githubusercontent.com` is blocked, download the script through any
working proxy/mirror, or copy it from a local checkout.

## Quick start

```bash
chmod +x build_vpn_in_vpn.sh
./build_vpn_in_vpn.sh --warp-group "🚀 节点选择"
```

`--warp-group` must be a **proxy group that already exists in your WARP profile**.
Common names:

- `🚀 节点选择`
- `♻️ 自动选择`
- `🔄 故障转移`

If you use a different name, pass it explicitly.

The script asks for:

- Proton username (email);
- countries (default `JP,US,NL`);
- Proton password (the generator prompts; it is not echoed).

It writes:

```text
WT_CF_chain.merge.yaml
```

Then:

1. Open `WT_CF_chain.merge.yaml` and copy everything.
2. Clash Verge Rev → **Profiles → Global Merge (全局扩展配置)** → paste → save.
3. Select **your own WARP MASQUE profile** and enable **TUN**.
4. Proxy page → `🎮 WT-VPN` → `Proton-Free`.
5. First hop: `🚀 CF-WARP` is not used in the Merge version; the `dialer-proxy`
   is your `--warp-group`, so Proton's WireGuard traffic goes through that group.

> Global Merge applies to every profile while it is enabled. Remove it when you
> finish testing, or keep it only if you always want the Proton hop.

## Russia / blocking notes

If Proton's API or website is blocked on your ISP, route the **login** through
your working WARP/TUN setup:

```bash
./build_vpn_in_vpn.sh \
  --warp-group "🚀 节点选择" \
  --proxy http://127.0.0.1:7897
```

Or, without cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/LG-leo/WarThunder_Issue/main/build_vpn_in_vpn.sh \
  | bash -s -- --warp-group "🚀 节点选择" --proxy http://127.0.0.1:7897
```

- `7897` is Clash Verge's mixed port; change it if yours differs.
- This sets `HTTP_PROXY` / `HTTPS_PROXY` for the Proton generator only.
- While generating the Proton config, keep Clash on the **pure WARP** profile,
  not on the chain profile; otherwise the login can loop through the unfinished chain.
- The generated profile still uses WARP as the first hop.
- GitHub release downloads may also be blocked; the script verifies the
  generator's SHA-256, but if `github.com` is unreachable, download
  `protonvpn-wg-confgen` manually and pass `--gen /path/to/binary`.

## Security

Generated files contain private keys:

- `protonvpn.conf` — Proton WireGuard private key;
- `WT_CF_chain.merge.yaml` — Proton private key (and no WARP key).

They are listed in `.gitignore`. Do not commit or share them.

## Field test (single session, 2026-11-16)

War Thunder, same network, roughly one evening. These are single-session
numbers, not a controlled benchmark.

| Configuration | Ping (ms) | Packet loss | Note |
|---|---:|---:|---|
| Old profile | 589–667 | 14–24% (avg 19%) | baseline |
| `WT_CF.yaml` (2–4 UDP paths) | 561–707 | 5–25% (avg 16%) | server accepted multiple egresses, but ping/PL jumped |
| `WT_CF_chain.yaml` (WARP → Proton NL) | **306–359** | **8–18% (avg 10%)** | best overall |
| New pure WARP profile | 417–771 | 8–17% | large jitter |
| Direct at 18:00 | 210–304 | 12% | lowest ping, but ISP QoS is intermittent |

Conclusions from this sample:

- The WARP→Proton chain supports the AS13335-QoS hypothesis: latency dropped
  by roughly 300 ms versus pure WARP, and jitter was much smaller.
- Multi-path UDP was accepted by the game server, but did not beat the chain:
  different WARP egresses have different RTTs, so replies arrive out of order
  and ping/PL jump. It is not the recommended daily driver.
- The selected Proton exit was in the **Netherlands** (WorldStream). For an
  Asian player, a **Japan** Proton free server may be closer; regenerate with
  `--countries JP` and compare.
- Direct connection is still the lowest-latency option when the ISP is not
  throttling; the chain is the more stable option during peak/QoS windows.

Possible next tests:

1. `--countries JP` vs `US` vs `NL` for the Proton hop.
2. Pick a specific WARP node as the first hop instead of `♻️ 自动选择`.
3. Try WireGuard MTU `1380` or `1400` if PL stays high.
4. Keep `WT_CF.yaml` multi-path as an experiment only; do not use it as the
   default profile.

## Limitations

- Proton free has limited locations and speed; it may be crowded.
- Two tunnels add latency; test several countries.
- War Thunder may treat the Proton egress differently; there is no public
  documentation that guarantees multi-hop/VPN egress is accepted.
- Check Proton's terms and your local laws before using this.

## Русский

`build_vpn_in_vpn.sh` добавляет бесплатный **Proton VPN (WireGuard)** перед
вашим собственным профилем **WARP MASQUE** в Clash Verge Rev.

```bash
chmod +x build_vpn_in_vpn.sh
./build_vpn_in_vpn.sh --warp-group "🚀 节点选择"
```

Если API Proton заблокирован, используйте прокси вашего WARP/Clash
(при генерации держите включённым **чистый WARP**, а не цепочку):

```bash
./build_vpn_in_vpn.sh \
  --warp-group "🚀 节点选择" \
  --proxy http://127.0.0.1:7897
```

Or, without cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/LG-leo/WarThunder_Issue/main/build_vpn_in_vpn.sh \
  | bash -s -- --warp-group "🚀 节点选择" --proxy http://127.0.0.1:7897
```

Затем вставьте содержимое `WT_CF_chain.merge.yaml` в
**Profiles → Global Merge** в Clash Verge Rev, включите TUN и выберите
`🎮 WT-VPN → Proton-Free`.

Скрипт **не содержит ключей WARP**. У каждого пользователя должен быть свой
профиль WARP MASQUE. Сгенерированные файлы содержат приватный ключ Proton —
не публикуйте их.

## Citation

If you reference this in a post, README, or video, link to:

- Guide: `https://github.com/LG-leo/WarThunder_Issue/blob/main/VPN_IN_VPN.md`
- Script: `https://github.com/LG-leo/WarThunder_Issue/blob/main/build_vpn_in_vpn.sh`
- One-line:
  `curl -fsSL https://raw.githubusercontent.com/LG-leo/WarThunder_Issue/main/build_vpn_in_vpn.sh | bash`

Short description:

> WARP MASQUE -> Proton VPN Free -> Gaijin chain for War Thunder, intended to
> avoid last-mile QoS on Cloudflare AS13335. The script adds a free Proton
> WireGuard hop in front of the user's own WARP profile; it does not ship WARP
> keys.

## Files

- `build_vpn_in_vpn.sh` — the public, key-free generator.
- `.gitignore` — keeps generated key files out of git.

The older local-only files (`WT_CF.yaml`, `WT_CF_chain.yaml`,
`warp-Cloudflare-AS13335-masque.yaml`) contain private keys and are not part of
this public tool.
