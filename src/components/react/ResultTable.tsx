import { formatCell } from '../../lib/compare.js';
type Props = { columns: string[]; rows: any[][]; max?: number; mark?: 'bad' | 'good' };
export default function ResultTable({ columns, rows, max = 200, mark }: Props) {
  const shown = rows.slice(0, max);
  return (
    <div>
      <div className="table-wrap">
        <table className="data">
          <thead><tr>{columns.map((c, i) => <th key={i}>{c}</th>)}</tr></thead>
          <tbody>
            {shown.map((r, i) => (
              <tr key={i} className={mark}>
                {r.map((v, j) => <td key={j} className={v === null ? 'null' : undefined}>{formatCell(v)}</td>)}
              </tr>
            ))}
            {shown.length === 0 && <tr><td colSpan={Math.max(1, columns.length)} className="null">No rows</td></tr>}
          </tbody>
        </table>
      </div>
      <p className="muted" style={{ fontSize: '.75rem', margin: '.25rem 0 0' }}>
        {rows.length} row{rows.length === 1 ? '' : 's'}{rows.length > max ? ` (showing first ${max})` : ''}
      </p>
    </div>
  );
}
