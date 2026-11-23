export type Result = { columns: string[]; rows: any[][] } | { value: any };
export const TOL: number;
export function compareResults(actual: Result | null, expected: Result | null | undefined, opts?: { orderMatters?: boolean }): { pass: boolean; message: string; missing: any[][]; extra: any[][] };
export function formatCell(v: any): string;
