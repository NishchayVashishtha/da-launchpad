// Components auto-mapped into every MDX file (no imports needed in content).
import Tip from './Tip.astro';
import Warning from './Warning.astro';
import InterviewAlert from './InterviewAlert.astro';
import RealWorld from './RealWorld.astro';
import CommonMistake from './CommonMistake.astro';
import InterviewQ from './InterviewQ.astro';
import FurtherReading from './FurtherReading.astro';
import FormulaCard from './FormulaCard.astro';
import Download from './Download.astro';
import A from './A.astro';
import PracticeSet from '../PracticeSet.astro';
import Quiz from './Quiz.astro';
import SqlPlayground from './SqlPlayground.astro';
import Mermaid from './Mermaid.astro';

export const mdxComponents = {
  Tip, Warning, InterviewAlert, RealWorld, CommonMistake, InterviewQ, FurtherReading, FormulaCard, Download, PracticeSet,
  a: A,
  Quiz, SqlPlayground, Mermaid,
};
