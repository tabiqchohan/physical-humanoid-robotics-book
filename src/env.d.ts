// TypeScript ko import.meta.env ka type batana
interface ImportMetaEnv {
  readonly REACT_APP_BACKEND_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
