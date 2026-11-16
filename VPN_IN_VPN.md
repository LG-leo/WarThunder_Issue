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

Затем вставьте содержимое `WT_CF_chain.merge.yaml` в
**Profiles → Global Merge** в Clash Verge Rev, включите TUN и выберите
`🎮 WT-VPN → Proton-Free`.

Скрипт **не содержит ключей WARP**. У каждого пользователя должен быть свой
профиль WARP MASQUE. Сгенерированные файлы содержат приватный ключ Proton —
не публикуйте их.

## Files

- `build_vpn_in_vpn.sh` — the public, key-free generator.
- `.gitignore` — keeps generated key files out of git.

The older local-only files (`WT_CF.yaml`, `WT_CF_chain.yaml`,
`warp-Cloudflare-AS13335-masque.yaml`) contain private keys and are not part of
this public tool.
