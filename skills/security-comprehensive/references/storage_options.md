# Secure Storage Options

## Windows

- Prefer Windows Credential Manager for user-scoped credentials.
- Use DPAPI for local encrypted blobs when Windows-only deployment is acceptable.

## Cross Platform

- Prefer `keyring` when the runtime and packaging model support it.
- Use encrypted local storage only with clear key-management rules.

## Migration Checklist

- Inventory existing storage.
- Preserve backward compatibility.
- Migrate on first successful login or controlled startup.
- Verify old plain-text values are removed or invalidated.
- Add tests that search storage for raw secret values.
