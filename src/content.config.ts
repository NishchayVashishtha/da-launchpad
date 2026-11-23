import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { MODULE_SLUGS } from './lib/modules';
import { jsonArrayLoader } from './lib/loaders';

const moduleEnum = z.enum(MODULE_SLUGS);
const difficulty = z.enum(['easy', 'medium', 'hard']);
const freq = z.enum(['low', 'medium', 'high']);

const lessons = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/lessons' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    module: moduleEnum,
    order: z.number(),
    estimatedMinutes: z.number(),
    objectives: z.array(z.string()).min(1),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const expectedOutput = z.union([
  z.object({ columns: z.array(z.string()), rows: z.array(z.array(z.any())) }),
  z.object({ value: z.any() }),
]);

const practice = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/practice' }),
  schema: z
    .object({
      id: z.string(),
      module: moduleEnum,
      topic: z.string(),
      difficulty,
      language: z.enum(['sql', 'python', 'excel', 'dax', 'text']),
      question: z.string(),
      dataset: z.string(),
      hint: z.string(),
      solutionSql: z.string().optional(),
      solutionCode: z.string().optional(),
      solution: z.string().optional(),
      expectedOutput: expectedOutput.optional(),
      orderMatters: z.boolean().default(false),
      explanation: z.string(),
      commonMistake: z.string(),
      interviewFrequency: freq,
      estimatedMinutes: z.number(),
      tags: z.array(z.string()).default([]),
    })
    .superRefine((q, ctx) => {
      if (q.language === 'sql' && !q.solutionSql) ctx.addIssue({ code: 'custom', message: 'sql question needs solutionSql' });
      if (q.language === 'python' && !q.solutionCode) ctx.addIssue({ code: 'custom', message: 'python question needs solutionCode' });
      if (['excel', 'dax', 'text'].includes(q.language) && !q.solution) ctx.addIssue({ code: 'custom', message: `${q.language} question needs solution` });
    }),
});

const interview = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/interview' }),
  schema: z.object({
    id: z.string(),
    category: z.string(),
    question: z.string(),
    whatInterviewerIsTesting: z.string(),
    modelAnswer: z.string(),
    followUps: z.array(z.string()).default([]),
    commonMistakes: z.array(z.string()).default([]),
    difficulty,
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/projects' }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    businessProblem: z.string(),
    datasetDescription: z.string(),
    skillsUsed: z.array(z.string()),
    steps: z.array(z.string()),
    deliverables: z.array(z.string()),
    readmeTemplate: z.string(),
    interviewTalkingPoints: z.array(z.string()),
    extensions: z.array(z.string()).default([]),
    estimatedHours: z.number(),
    order: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

const flashcards = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/flashcards' }),
  schema: z.object({ id: z.string(), topic: z.string(), front: z.string(), back: z.string() }),
});

const glossary = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/glossary' }),
  schema: z.object({
    id: z.string(),
    term: z.string(),
    definition: z.string(),
    example: z.string().optional(),
    related: z.array(z.string()).optional(),
  }),
});

const mcq = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/mcq' }),
  schema: z.object({
    id: z.string(),
    module: moduleEnum,
    topic: z.string(),
    section: z.string().optional(),
    difficulty,
    question: z.string(),
    options: z.array(z.string()).min(2),
    answerIndex: z.number().int().min(0),
    explanation: z.string(),
    shortcut: z.string().optional(),
  }),
});

const cases = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/cases' }),
  schema: z.object({
    title: z.string(),
    industry: z.string(),
    difficulty,
    type: z.enum(['case-study', 'mock-case', 'take-home']),
    estimatedMinutes: z.number(),
    draft: z.boolean().default(false),
  }),
});

const tests = defineCollection({
  loader: jsonArrayLoader({ base: './src/content/tests' }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    durationMinutes: z.number(),
    questionIds: z.array(z.string()).min(1),
  }),
});

export const collections = { lessons, practice, interview, projects, flashcards, glossary, mcq, cases, tests };
