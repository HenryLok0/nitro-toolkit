# Nitro 

[![Code Size](https://img.shields.io/github/languages/code-size/HenryLok0/nitro-toolkit?style=flat-square&logo=github)](https://github.com/HenryLok0/nitro-toolkit)
![PyPI - Version](https://img.shields.io/pypi/v/nitro-toolkit)

[![MIT License](https://img.shields.io/github/license/HenryLok0/nitro-toolkit?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/HenryLok0/nitro-toolkit?style=flat-square)](https://github.com/HenryLok0/nitro-toolkit/stargazers)

Discord Nitro gift code generator and checker toolkit.

## ⚠️ Important Warning

**This tool is for educational purposes only. Please comply with Discord's Terms of Service.**

- Do not use this tool to violate Discord's ToS
- Excessive API requests may result in IP bans
- Use at your own risk and responsibility
- The author is not responsible for any consequences

## Features

- Generate Discord Nitro Classic and Boost codes
- Batch check gift card link validity
- Proxy support with automatic rotation
- Multi-threading for faster processing
- Smart rate limiting protection
- JSON result export

## Installation

```bash
pip install nitro-toolkit
```

## Quick Start

```bash
# Run the integrated tool
nitro-toolkit

# Basic usage
codestate [options]
```

## Options

| Option                  | Description |
|-------------------------|-------------|
| `--gen-proxies`         | Download fresh proxies to data/proxies.txt and exit |
| `--use-proxy`           | Enable proxy mode (load proxies from data/proxies.txt) |
| `--input`, `-i`         | Input file path (containing gift card links) |
| `--delay`, `-d`         | Request delay (seconds, default: 1.0) |
| `--timeout`, `-t`       | Request timeout (seconds, default: 10) |
| `--workers`, `-w`       | Max concurrent workers (default: 5) |
| `--no-threading`        | Disable multi-threading |
| `--output`, `-o`        | Output filename |
| `--proxy-file`          | Proxy list file path (default: data/proxies.txt) |

## Important Notes

- Valid codes are extremely rare (1 in millions)
- Use proxies to avoid IP blocking
- Respect Discord's Terms of Service
- Start with small batches for testing

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you have questions or need help, please open an issue on GitHub.

Thank you to all contributors and the open-source community for your support.
