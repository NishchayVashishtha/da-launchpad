#!/usr/bin/env python3
"""Generate aptitude and screening MCQs for the Interview Prep module.

Deterministic: each section has its own fixed seed. Correct answers are
computed in code (exact Fractions, model checks, brute-force solvers).
The only hand-written data is the short verbal list at the bottom.

Writes src/content/mcq/aptitude-<section>.json (module "interview").

Usage: .venv/bin/python scripts/generate_aptitude.py
"""
from __future__ import annotations

import json
import random
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial, gcd, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "src" / "content" / "mcq"
SEED = "da-launchpad-aptitude-v1"
LEVELS = ("easy", "medium", "hard")
ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth"]

NAMES = [
    "Asha", "Ravi", "Meera", "Kiran", "Priya", "Arjun", "Divya", "Rohan",
    "Sneha", "Vikram", "Nisha", "Farhan", "Anita", "Suresh", "Lakshmi", "Imran",
    "Tara", "Deepak", "Gita", "Manoj", "Kavya", "Harish", "Ritu", "Sanjay",
]
COMPANIES = [
    "Vaidehi Agro", "Brindavan Tech", "Tungabhadra Logistics", "Meghna Pharma",
    "Chilika Textiles", "Narmada Foods", "Godavari Motors", "Sahyadri Steel",
]


class Retry(Exception):
    """Raised by a template when generated numbers do not fit its rules."""


def R(cond: bool) -> None:
    if not cond:
        raise Retry()


# ---------------------------------------------------------------- formatting

def dec(x, places: int = 2) -> str:
    """Exact value rounded half-up, trailing zeros removed."""
    x = F(x)
    q = Decimal(x.numerator) / Decimal(x.denominator)
    q = q.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    s = format(q, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def grp(int_str: str) -> str:
    """Indian digit grouping: 1,23,45,678."""
    if len(int_str) <= 3:
        return int_str
    head, tail = int_str[:-3], int_str[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def rs(x) -> str:
    x = F(x)
    s = dec(abs(x), 2)
    ip, _, fp = s.partition(".")
    out = "₹" + grp(ip) + ("." + fp if fp else "")
    return "-" + out if x < 0 else out


def pct(x, places: int = 2) -> str:
    return dec(x, places) + "%"


def num(x, unit: str = "", places: int = 2) -> str:
    return dec(x, places) + (" " + unit if unit else "")


def frac(x) -> str:
    x = F(x)
    return f"{x.numerator}/{x.denominator}"


def ratio_str(a: int, b: int) -> str:
    g = gcd(a, b)
    return f"{a // g}:{b // g}"


# ---------------------------------------------------------------- quant

def p_percent(rng, lvl):
    if lvl == "easy":
        p = rng.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75, 80, 120, 150])
        n = rng.randrange(400, 9001, 50)
        v = F(n * p, 100)
        return {
            "q": f"What is {p}% of ₹{grp(str(n))}?",
            "correct": rs(v),
            "dist": [rs(F(n * p, 10)), rs(F(n, p) * 100), rs(n * p), rs(n - v), rs(F(n * p, 1000))],
            "why": f"{p}% means {p}/100. So {p}% of {n} = {n} × {p} ÷ 100 = {rs(v)}.",
            "tip": "Find 10% first (divide by 10), then scale it up.",
        }
    if lvl == "medium":
        a = rng.choice(range(20, 51, 5))
        b = rng.choice(range(5, a // 2 + 1, 5))
        net = F(a) - b - F(a * b, 100)
        R(net > 0)
        after_rise = 100 + a
        final = F(after_rise * (100 - b), 100)
        return {
            "q": f"The price of a product goes up by {a}% and then comes down by {b}%. What is the overall percent change?",
            "correct": f"{pct(net)} increase",
            "dist": [f"{dec(a - b)}% increase", f"{dec(a + b)}% increase",
                     f"{dec(F(a * b, 100))}% decrease", f"{dec(a - b + F(a * b, 100))}% increase"],
            "why": (f"Start at 100. After the {a}% rise it is {after_rise}. "
                    f"The {b}% fall acts on {after_rise}, so the price is {after_rise} × {100 - b}/100 = {dec(final)}. "
                    f"Change = {dec(final)} − 100 = {dec(net)}%. Adding or subtracting the two percents misses the second base."),
            "tip": "Use 100 as the base. Multiply the factors: (1 + a/100)(1 − b/100).",
        }
    a = rng.choice(range(10, 41, 5))
    b = rng.choice(range(10, 41, 5))
    v = F((100 + a) * (100 - b), 100)
    return {
        "q": (f"Ravi's salary is {a}% more than Sunil's. Sunil's salary is {b}% less than Manoj's. "
              "Ravi's salary is what percent of Manoj's?"),
        "correct": pct(v),
        "dist": [pct(100 + a - b), pct(100 + a + b), pct(F((100 + a) * (100 + b), 100)), pct(a - b)],
        "why": (f"Take Manoj's salary as 100. Sunil = 100 × (1 − {b}/100) = {dec(F(100 - b))}. "
                f"Ravi = {dec(F(100 - b))} × (1 + {a}/100) = {dec(v)}. So Ravi is {pct(v)} of Manoj."),
        "tip": "Two chained changes: multiply the factors, never add the percents.",
    }


def p_ratio(rng, lvl):
    if lvl == "easy":
        p, q = rng.sample(range(2, 10), 2)
        S = (p + q) * rng.randrange(5, 60)
        big, small = max(p, q), min(p, q)
        v = F(S * big, p + q)
        a, b = rng.sample(NAMES, 2)
        return {
            "q": (f"The savings of {a} and {b} are in the ratio {p}:{q}. Together they saved ₹{grp(str(S))}. "
                  "How much did the person with the larger share save?"),
            "correct": rs(v),
            "dist": [rs(F(S * small, p + q)), rs(F(S, 2)), rs(F(S * big, small)), rs(S - v)],
            "why": (f"The parts add up to {p + q}. One part is ₹{grp(str(S))} ÷ {p + q} = {rs(F(S, p + q))}. "
                    f"The larger share is {big} parts = {rs(v)}."),
            "tip": "Add the ratio parts, find the value of one part, then multiply.",
        }
    if lvl == "medium":
        p, q, r, s = (rng.randrange(2, 10) for _ in range(4))
        return {
            "q": f"The ratio of Asha's age to Ravi's age is {p}:{q}. The ratio of Ravi's age to Meera's age is {r}:{s}. What is the ratio of Asha's age to Meera's age?",
            "correct": ratio_str(p * r, q * s),
            "dist": [ratio_str(p + r, q + s), ratio_str(p * s, q * r), ratio_str(p, q), ratio_str(r, s), ratio_str(p * q, r * s)],
            "why": (f"Asha/Meera = (Asha/Ravi) × (Ravi/Meera) = ({p}/{q}) × ({r}/{s}) = {p * r}/{q * s}. "
                    f"So Asha : Meera = {ratio_str(p * r, q * s)} in simplest form."),
            "tip": "Chain ratios by multiplying the first parts and the second parts. Do not add them.",
        }
    p, q = rng.sample(range(1, 9), 2)
    r, s = rng.sample(range(1, 9), 2)
    d = rng.randrange(2, 20)
    den = p * s - r * q
    R(den > 0)
    R((r * d) % den == 0)
    t = r * d // den
    men, women = p * t, q * t
    R(men > 0 and women > 0)
    assert men * s == r * (women + d)
    total = men + women
    return {
        "q": (f"In a class, the ratio of men to women is {p}:{q}. After {d} more women join, "
              f"the ratio of men to women becomes {r}:{s}. How many students were in the class at first?"),
        "correct": f"{total} students",
        "dist": [f"{men} students", f"{women + d} students", f"{total + d} students", f"{men + women + 2 * d} students"],
        "why": (f"Let the common factor be t. Men = {p}t, women = {q}t. Then {p}t × {s} = {r} × ({q}t + {d}), "
                f"so t = {r * d} ÷ {den} = {t}. Men = {men}, women = {women}, total = {total}."),
        "tip": "Set up the cross-multiplied equation with one unknown factor t.",
    }


def p_avg(rng, lvl):
    if lvl == "easy":
        n = rng.randrange(4, 11)
        A = rng.randrange(40, 81)
        b = rng.randrange(20, 101)
        v = F(n * A + b, n + 1)
        return {
            "q": f"The average score of {n} students in a test is {A}. A new student who scored {b} joins. What is the new average?",
            "correct": num(v),
            "dist": [num(F(A + b, 2)), num(n * A + b), num(A + F(b, n + 1)), num(F(n * A, n + 1))],
            "why": f"Total of {n} scores = {n} × {A} = {n * A}. Add {b}: total = {n * A + b} for {n + 1} students. Average = {dec(v)}.",
            "tip": "New average = (old total + new value) ÷ new count.",
        }
    if lvl == "medium":
        n = rng.randrange(8, 21)
        k = rng.randrange(2, n - 2)
        A = rng.randrange(20, 50)
        B = rng.randrange(A + 1, A + 15)
        v = F(n * B - k * A, n - k)
        R(v > 0)
        return {
            "q": (f"The average age of the first {k} members of a club is {A} years. The average age of all {n} members "
                  f"is {B} years. What is the average age of the other {n - k} members?"),
            "correct": num(v, "years"),
            "dist": [num(F(A + B, 2), "years"), num(B - A, "years"), num(F(n * B, n - k), "years"), num(F(k * A, n), "years")],
            "why": (f"Total of all {n} = {n} × {B} = {n * B}. Total of first {k} = {k} × {A} = {k * A}. "
                    f"Rest total = {n * B - k * A} shared by {n - k} members = {dec(v)} years."),
            "tip": "Average × count gives the total. Subtract totals, then divide by the leftover count.",
        }
    x = rng.randrange(10, 30)
    y = rng.randrange(10, 30)
    w1 = rng.randrange(30, 60)
    w2 = rng.randrange(30, 60)
    v = F(x * w1 + y * w2, x + y)
    return {
        "q": (f"A class has {x} boys with an average weight of {w1} kg and {y} girls with an average weight of {w2} kg. "
              "What is the average weight of the whole class?"),
        "correct": num(v, "kg"),
        "dist": [num(F(w1 + w2, 2), "kg"), num(x * w1 + y * w2, "kg"), num(F(w1, x) + F(w2, y), "kg"), num(F(x * w1, x + y) + F(w2, 2), "kg")],
        "why": (f"Boys' total = {x} × {w1} = {x * w1}. Girls' total = {y} × {w2} = {y * w2}. "
                f"Class total = {x * w1 + y * w2} over {x + y} students = {dec(v)} kg."),
        "tip": "Weighted average: add the totals, then divide by the total count. Simple averages are wrong here.",
    }


def p_pl(rng, lvl):
    if lvl == "easy":
        c = rng.randrange(200, 5001, 100)
        p = rng.choice([5, 10, 12, 15, 20, 25, 30, 40])
        v = F(c * (100 + p), 100)
        return {
            "q": f"An item costs the shopkeeper ₹{grp(str(c))}. He sells it at a profit of {p}%. What is the selling price?",
            "correct": rs(v),
            "dist": [rs(c + p), rs(F(c * p, 100)), rs(F(c * (100 - p), 100)), rs(c * p)],
            "why": f"Selling price = cost + {p}% of cost = {c} × {100 + p}/100 = {rs(v)}.",
            "tip": "Selling price = cost × (100 + profit%) ÷ 100.",
        }
    if lvl == "medium":
        M = rng.randrange(800, 9001, 100)
        d = rng.choice([10, 20, 25, 30])
        p = rng.choice([10, 15, 20, 25])
        sp = F(M * (100 - d), 100)
        cp = sp * 100 / (100 + p)
        return {
            "q": (f"A shirt has a marked price of ₹{grp(str(M))}. The shop gives a {d}% discount and still earns "
                  f"a {p}% profit on its cost price. What is the cost price?"),
            "correct": rs(cp),
            "dist": [rs(sp), rs(F(sp * (100 + p), 100)), rs(F(M * (100 - d - p), 100)), rs(F(M * (100 + p), 100))],
            "why": (f"Selling price = {M} less {d}% = {rs(sp)}. Profit is on cost, so SP = cost × {100 + p}/100. "
                    f"Cost = {rs(sp)} × 100 ÷ {100 + p} = {rs(cp)}."),
            "tip": "Undo the steps in reverse: divide by (100 + profit%) last.",
        }
    if rng.random() < 0.5:
        m = rng.choice([10, 20, 25, 30, 40])
        d = rng.choice([5, 10, 15, 20])
        v = F((100 + m) * (100 - d) - 10000, 100)
        R(v > 0)
        return {
            "q": f"A shopkeeper marks goods {m}% above cost price and then gives a {d}% discount on the marked price. What is his profit percent?",
            "correct": pct(v),
            "dist": [pct(m - d), pct(m + d), pct(F(m * (100 - d), 100)), pct(m - d + F(m * d, 100))],
            "why": (f"Take cost = 100. Marked price = {100 + m}. Selling price = {100 + m} × {100 - d}/100 = {dec(F((100 + m) * (100 - d), 100))}. "
                    f"Profit = {dec(F((100 + m) * (100 - d), 100))} − 100 = {dec(v)}%. Subtracting m − d ignores that the discount acts on a bigger base."),
            "tip": "Profit % ≈ markup − discount − (markup × discount)/100.",
        }
    x = rng.choice([10, 20, 30, 40])
    v = F(x * x, 100)
    return {
        "q": (f"A trader sells two identical items at the same price. On one he makes a profit of {x}% and "
              f"on the other he makes a loss of {x}%. What is his overall result?"),
        "correct": f"a loss of {dec(v)}%",
        "dist": ["no profit and no loss", f"a profit of {dec(v)}%", f"a loss of {x}%", f"a profit of {x}%"],
        "why": (f"Let each selling price be 100. Cost of the first item = 100/(1 + {x}/100), "
                f"cost of the second = 100/(1 − {x}/100). Total cost is more than total sale, so there is an overall loss "
                f"of {x}² ÷ 100 = {dec(v)}% of cost."),
        "tip": "Equal profit and loss percents never cancel. The net result is always a loss of x²/100 %.",
    }


def p_si(rng, lvl):
    if lvl == "easy":
        P = rng.randrange(2, 30) * 1000
        r = rng.choice([4, 5, 6, 7, 8, 9, 10, 12])
        T = rng.randrange(2, 8)
        v = F(P * r * T, 100)
        return {
            "q": f"What simple interest does ₹{grp(str(P))} earn at {r}% per year for {T} years?",
            "correct": rs(v),
            "dist": [rs(P * r * T), rs(F(P * r, 100)), rs(P + v), rs(F(P * r * T, 10))],
            "why": f"SI = P × R × T ÷ 100 = {P} × {r} × {T} ÷ 100 = {rs(v)}.",
            "tip": "Find 1% of P, then multiply by R × T.",
        }
    if lvl == "medium":
        P = rng.randrange(2, 20) * 1000
        r = rng.choice([4, 5, 6, 8, 10, 12])
        T = rng.choice([2, 3, 4, 5, 6])
        I = F(P * r * T, 100)
        return {
            "q": f"₹{grp(str(P))} becomes ₹{grp(str(P + I))} in {T} years at simple interest. What is the rate per year?",
            "correct": f"{r}% per year",
            "dist": [f"{pct(F(100 * I, P))} per year", f"{pct(F(I, P * T))} per year",
                     f"{pct(F(100 * I, P + I))} per year", f"{r + 2}% per year"],
            "why": (f"Interest = {rs(I)}. Rate = 100 × SI ÷ (P × T) = 100 × {rs(I)} ÷ ({P} × {T}) = {r}%."),
            "tip": "Rate = 100 × SI ÷ (P × T). Do not forget the 100 and the time.",
        }
    r = rng.choice([2, 4, 5, 8, 10, 20, 25])
    return {
        "q": f"At {r}% simple interest per year, in how many years will an amount double (earn interest equal to the principal)?",
        "correct": num(F(100, r), "years"),
        "dist": [num(F(50, r), "years"), num(F(200, r), "years"), num(F(r, 100), "years"), num(100 * r, "years")],
        "why": f"Interest per year = P × {r}/100. For interest to equal P, T × {r}/100 = 1, so T = 100 ÷ {r} = {dec(F(100, r))} years.",
        "tip": "At simple interest, years to double = 100 ÷ rate.",
    }


def p_ci(rng, lvl):
    if lvl == "easy":
        P = rng.randrange(1, 30) * 1000
        r = rng.choice([5, 8, 10, 12, 20])
        n = rng.choice([2, 3])
        g = F(100 + r, 100)
        v = P * g ** n
        return {
            "q": f"₹{grp(str(P))} is invested at {r}% per year, compounded yearly. What is the amount after {n} years?",
            "correct": rs(v),
            "dist": [rs(P * (1 + F(r * n, 100))), rs(P * g ** (n + 1)), rs(P * g ** (n - 1)), rs(F(P * r * n, 100))],
            "why": f"Amount = P × (1 + r/100)^n = {P} × ({100 + r}/100)^{n} = {rs(v)}.",
            "tip": "Compound growth multiplies by (1 + r/100) each year. Simple interest adds the same amount each year.",
        }
    if lvl == "medium":
        P = rng.randrange(1, 12) * 10000
        r = rng.randrange(5, 25)
        diff = P * F(r, 100) ** 2
        return {
            "q": f"What is the difference between compound interest and simple interest on ₹{grp(str(P))} for 2 years at {r}% per year?",
            "correct": rs(diff),
            "dist": [rs(F(P * 2 * r, 100)), rs(F(P * r, 100)), rs(P * F(2 * r, 100) + diff), rs(F(P * r * r, 100))],
            "why": (f"CI for 2 years = P[(1 + r/100)² − 1]. SI = P × 2 × r/100 = {rs(F(P * 2 * r, 100))}. "
                    f"The difference is P × (r/100)² = {rs(diff)}."),
            "tip": "Difference over 2 years at rate r = P × (r/100)².",
        }
    P = rng.randrange(1, 20) * 10000
    r = rng.choice([4, 6, 8, 10, 12, 20])
    n = rng.choice([1, 2])
    v = P * F(200 + r, 200) ** (2 * n)
    return {
        "q": f"₹{grp(str(P))} is invested at {r}% per year, compounded half-yearly. What is the amount after {n} year(s)?",
        "correct": rs(v),
        "dist": [rs(P * F(100 + r, 100) ** n), rs(P * F(100 + r, 100) ** (2 * n)), rs(P * (1 + F(r * n, 100))),
                 rs(P * F(200 + r, 200) ** n)],
        "why": (f"Half-yearly means rate r/2 for 2n periods: A = P(1 + r/200)^(2n) = {P} × ({200 + r}/200)^{2 * n} = {rs(v)}."),
        "tip": "Half-yearly compounding: halve the rate and double the number of periods.",
    }


def p_tw(rng, lvl):
    choices = [6, 8, 10, 12, 15, 20, 24, 30]
    if lvl == "easy":
        a, b = rng.sample(choices, 2)
        v = F(a * b, a + b)
        return {
            "q": f"Asha can finish a job in {a} days. Ravi can finish the same job in {b} days. How many days will they take working together?",
            "correct": num(v, "days"),
            "dist": [num(F(a + b, 2), "days"), num(a * b, "days"), num(a + b, "days"), num(F(min(a, b), 2), "days")],
            "why": (f"Work per day: Asha 1/{a}, Ravi 1/{b}. Together 1/{a} + 1/{b} = {a + b}/{a * b}. "
                    f"Days = {a * b}/{a + b} = {dec(v)} days."),
            "tip": "Two workers together take (a × b) ÷ (a + b) days.",
        }
    if lvl == "medium":
        a, b = rng.sample(choices, 2)
        lim = (a * b) // (a + b)
        R(lim >= 2)
        t = rng.randrange(1, lim)
        left = 1 - t * (F(1, a) + F(1, b))
        v = b * left
        R(v > 0)
        return {
            "q": (f"Asha takes {a} days alone to finish a work and Ravi takes {b} days alone. They work together "
                  f"for {t} days, then Asha leaves. How many more days will Ravi need to finish the rest?"),
            "correct": num(v, "days"),
            "dist": [num(b - t, "days"), num(b * (1 - F(t, a)), "days"), num(b * (1 - F(t, b)), "days"), num(a - t, "days")],
            "why": (f"Together in {t} days they finish {t} × (1/{a} + 1/{b}) = {dec(t * (F(1, a) + F(1, b)))} of the work. "
                    f"Work left = {dec(left)}. Ravi alone does 1/{b} a day, so he needs {b} × {dec(left)} = {dec(v)} days."),
            "tip": "Find the work done together, subtract from 1, then multiply by the other person's total days.",
        }
    while True:
        a, c, b = rng.sample([6, 8, 10, 12, 15, 20, 24, 30, 40, 60], 3)
        net = F(1, a) + F(1, c) - F(1, b)
        if net > 0:
            break
    v = 1 / net
    return {
        "q": (f"Pipe X fills an empty tank in {a} hours. Pipe Y fills it in {c} hours. Pipe Z empties a full tank "
              f"in {b} hours. If all three pipes are open and the tank is empty, how many hours will it take to fill it?"),
        "correct": num(v, "hours"),
        "dist": [num(1 / (F(1, a) + F(1, c) + F(1, b)), "hours"), num(1 / (F(1, a) + F(1, c)), "hours"),
                 num(F(a + c, 2), "hours"), num(b, "hours")],
        "why": (f"Filling rate = 1/{a} + 1/{c}. Emptying rate = 1/{b}. Net rate = {dec(net, 4)} tank per hour. "
                f"Time = 1 ÷ net = {dec(v)} hours."),
        "tip": "Net rate = fill rates minus the empty rate. Time = 1 ÷ net rate.",
    }


def p_tsd(rng, lvl):
    if lvl == "easy":
        L = rng.randrange(1, 12) * 50
        T = rng.choice([4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30])
        v = F(L * 18, 5 * T)
        return {
            "q": f"A {L} m long train crosses a pole in {T} seconds. What is its speed in km/h?",
            "correct": num(v, "km/h"),
            "dist": [num(F(L, T), "km/h"), num(F(L * 5, 18 * T), "km/h"), num(F(L * T * 18, 5), "km/h"), num(F(L * 18, T), "km/h")],
            "why": f"Speed in m/s = {L} ÷ {T} = {dec(F(L, T))} m/s. Multiply by 18/5 to convert to km/h: {dec(v)} km/h.",
            "tip": "m/s × 3.6 = km/h. Multiply by 18 and divide by 5.",
        }
    if lvl == "medium":
        a, b = rng.sample(range(20, 61, 5), 2)
        v = F(2 * a * b, a + b)
        return {
            "q": (f"A bus travels from town P to town Q at {a} km/h and returns from Q to P at {b} km/h on the same road. "
                  "What is its average speed for the whole trip?"),
            "correct": num(v, "km/h"),
            "dist": [num(F(a + b, 2), "km/h"), num(F(a * b, a + b), "km/h"), num(a + b, "km/h"), num(F(a * b, 2), "km/h")],
            "why": (f"Take distance d each way. Time = d/{a} + d/{b}. Average = 2d ÷ (d/{a} + d/{b}) = 2×{a}×{b}/({a}+{b}) = {dec(v)} km/h. "
                    "The simple average of the two speeds is wrong when the distance is the same both ways."),
            "tip": "For equal distances, average speed = 2ab ÷ (a + b). Never just average the two speeds.",
        }
    L1 = rng.randrange(1, 10) * 50
    L2 = rng.randrange(1, 10) * 50
    s1 = rng.randrange(30, 81, 5)
    s2 = rng.randrange(30, 81, 5)
    R(s1 != s2)
    v = F((L1 + L2) * 18, 5 * (s1 + s2))
    return {
        "q": (f"Two trains of lengths {L1} m and {L2} m run on parallel tracks in opposite directions at {s1} km/h and "
              f"{s2} km/h. In how many seconds do they pass each other completely?"),
        "correct": num(v, "seconds"),
        "dist": [num(F(L1 + L2, s1 + s2), "seconds"), num(F((L1 + L2) * 5, 18 * (s1 + s2)), "seconds"),
                 num(F((L1 + L2) * 18, 5 * abs(s1 - s2)), "seconds"), num(F((L1 + L2) * 18, 5 * max(s1, s2)), "seconds")],
        "why": (f"Opposite directions: relative speed = {s1} + {s2} = {s1 + s2} km/h = {dec(F((s1 + s2) * 5, 18))} m/s. "
                f"Distance to clear = {L1} + {L2} = {L1 + L2} m. Time = {L1 + L2} ÷ {dec(F((s1 + s2) * 5, 18))} = {dec(v)} seconds."),
        "tip": "Opposite directions: add the speeds. Same direction: subtract them.",
    }


def p_prob(rng, lvl):
    if lvl == "easy":
        r = rng.randrange(3, 12)
        g = rng.randrange(3, 12)
        R(r != g)
        v = F(r, r + g)
        return {
            "q": f"A jar has {r} red marbles and {g} green marbles. One marble is picked at random without looking. What is the chance it is red? Give the answer as a fraction.",
            "correct": frac(v),
            "dist": [frac(F(g, r + g)), frac(F(r, g)), frac(F(1, r + g)), frac(F(r + g, r))],
            "why": f"There are {r + g} marbles. {r} are red. P(red) = {r}/{r + g} = {frac(v)}.",
            "tip": "Chance = favourable outcomes ÷ total outcomes.",
        }
    if lvl == "medium":
        N = rng.randrange(8, 21)
        r = rng.randrange(3, N - 2)
        g = N - r
        v = F(r * (r - 1), N * (N - 1))
        return {
            "q": (f"A box has {N} tickets. {r} of them are winners. Two tickets are drawn one after another without "
                  "replacement. What is the probability that both are winners? Give the answer as a fraction."),
            "correct": frac(v),
            "dist": [frac(F(r * r, N * N)), frac(F(r * (r - 1), N * N)), frac(F(r, N)), frac(F(2 * r * g, N * (N - 1)))],
            "why": (f"P(first wins) = {r}/{N}. Then {r - 1} winners are left among {N - 1} tickets, "
                    f"so P(second wins) = {r - 1}/{N - 1}. Multiply: {r} × {r - 1} / ({N} × {N - 1}) = {frac(v)}."),
            "tip": "Without replacement, reduce both the count and the total by one for the second draw.",
        }
    pool = [F(1, 2), F(1, 3), F(1, 4), F(2, 5), F(3, 5), F(1, 5), F(2, 3), F(3, 4)]
    p, q = rng.sample(pool, 2)
    v = 1 - (1 - p) * (1 - q)
    return {
        "q": (f"Two independent events have chances {frac(p)} and {frac(q)} of happening. "
              "What is the chance that at least one of them happens? Give the answer as a fraction."),
        "correct": frac(v),
        "dist": [frac(p * q), frac((1 - p) * (1 - q)), frac(1 - p * q), frac(p + q)],
        "why": (f"P(neither) = (1 − {frac(p)}) × (1 − {frac(q)}) = {frac((1 - p) * (1 - q))}. "
                f"P(at least one) = 1 − P(neither) = {frac(v)}."),
        "tip": "'At least one' is easiest as 1 minus 'none'.",
    }


def p_pc(rng, lvl):
    if lvl == "easy":
        n = rng.randrange(6, 13)
        r = rng.randrange(2, 5)
        v = comb(n, r)
        return {
            "q": f"In how many ways can a committee of {r} people be chosen from a club of {n} members?",
            "correct": str(v),
            "dist": [str(factorial(n) // factorial(n - r)), str(n ** r), str(comb(n, r + 1)), str(comb(n + 1, r))],
            "why": f"Order does not matter in a committee, so use nCr = {n}! ÷ ({r}! × {n - r}!) = {v}.",
            "tip": "Committee (order does not matter) = nCr. Seating or ranking (order matters) = nPr.",
        }
    if lvl == "medium":
        word = rng.choice(["LEVEL", "PEPPER", "BANANA", "SUCCESS", "COFFEE", "ASSESS", "LETTER", "RETAIL", "PAPPAD"])
        counts = Counter(word)
        n = len(word)
        den = prod(factorial(c) for c in counts.values())
        v = factorial(n) // den
        reps = [f"{c}!" for c in counts.values() if c > 1]
        return {
            "q": f"How many different arrangements can be made using all the letters of the word {word}?",
            "correct": str(v),
            "dist": [str(factorial(n)), str(factorial(n) // factorial(max(counts.values()))),
                     str(factorial(n) // 2), str(v * 2)],
            "why": (f"There are {n} letters. Swapping equal letters does not give a new arrangement, so divide by the "
                    f"factorial of each repeat count: {n}! ÷ ({' × '.join(reps)}) = {v}."),
            "tip": "Repeated letters: n! divided by the factorial of each repeat count.",
        }
    a = rng.randrange(4, 9)
    b = rng.randrange(3, 7)
    k = rng.choice([2, 3, 4])
    v = comb(a + b, k) - comb(a, k)
    R(v > 0)
    return {
        "q": (f"A team of {k} is to be picked from {a} men and {b} women. The team must have at least one woman. "
              "How many different teams are possible?"),
        "correct": str(v),
        "dist": [str(comb(a + b, k)), str(comb(b, k)), str(comb(a, k)), str(comb(a + b, k) - comb(b, k))],
        "why": (f"All teams = C({a + b},{k}) = {comb(a + b, k)}. Remove the teams with no woman, C({a},{k}) = {comb(a, k)}. "
                f"Answer = {comb(a + b, k)} − {comb(a, k)} = {v}."),
        "tip": "'At least one' = all possibilities minus the 'none' case.",
    }


def p_series(rng, lvl):
    kinds = ["arith", "geom", "square", "alt"] if lvl == "easy" else ["arith", "geom", "square", "alt", "mult", "incr"]
    kind = rng.choice(kinds)
    if kind == "arith":
        a = rng.randrange(1, 40)
        d = rng.randrange(2, 17)
        s = [a + i * d for i in range(6)]
        return {
            "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[5] + d), str(s[5] - 1), str(s[4]), str(s[5] + 2 * d), str(s[5] + d + 1)],
            "why": f"Each term adds {d}. The next term is {s[4]} + {d} = {s[5]}.",
            "tip": "Find the common difference, then add it again.",
        }
    if kind == "geom":
        a = rng.randrange(1, 6)
        r = rng.choice([2, 3])
        s = [a * r ** i for i in range(6)]
        return {
            "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[4] + s[3]), str(s[5] + a), str(s[5] - r), str(s[4] + r), str(s[4] * 2)],
            "why": f"Each term is the previous term × {r}. The next term is {s[4]} × {r} = {s[5]}.",
            "tip": "Divide a term by the one before it to find the ratio.",
        }
    if kind == "square":
        c = rng.randrange(0, 7)
        s = [(i + 1) ** 2 + c for i in range(6)]
        return {
            "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[5] + 1), str(s[5] - c), str(s[4] + 13), str(s[5] + c), str(s[5] - 1)],
            "why": f"The terms are n² + {c} for n = 1, 2, 3, ... The next term has n = 6: 6² + {c} = {s[5]}.",
            "tip": "Write the position number, square it, then add the constant.",
        }
    if kind == "alt":
        a = rng.randrange(1, 7)
        b = rng.randrange(2, 9)
        x0 = rng.randrange(1, 20)
        s = [x0]
        for i in range(5):
            s.append(s[-1] + (a if i % 2 == 0 else b))
        return {
            "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[4] + b), str(s[5] + b), str(s[5] - b), str(s[4] + 2 * a)],
            "why": f"The gaps alternate +{a} and +{b}. The next gap is +{a}, so the next term is {s[4]} + {a} = {s[5]}.",
            "tip": "When two steps alternate, check the gaps one by one.",
        }
    if kind == "mult":
        k = rng.choice([2, 3])
        c = rng.randrange(1, 6)
        x0 = rng.randrange(1, 5)
        s = [x0]
        for _ in range(5):
            s.append(s[-1] * k + c)
        return {
            "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[4] * k), str(s[5] + c), str(s[5] - c), str(s[4] + c), str(s[5] + k)],
            "why": f"Each term is the previous term × {k}, then + {c}. The next term is {s[4]} × {k} + {c} = {s[5]}.",
            "tip": "Test the rule on the first two terms before you trust it.",
        }
    d0 = rng.randrange(1, 5)
    e = rng.randrange(1, 4)
    x0 = rng.randrange(1, 10)
    s = [x0]
    inc = d0
    for _ in range(5):
        s.append(s[-1] + inc)
        inc += e
    return {
        "q": f"What number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
        "correct": str(s[5]),
        "dist": [str(s[4] + d0 + 2 * e), str(s[5] + 1), str(s[5] + e), str(s[4] + d0), str(s[4] + d0 + 3 * e)],
        "why": (f"The gaps grow by {e} each time. The next gap is {d0 + 4 * e}, so the next term is "
                f"{s[4]} + {d0 + 4 * e} = {s[5]}."),
        "tip": "When gaps grow by a fixed amount, write the gaps down first.",
    }


# ---------------------------------------------------------------- logical

def p_letters(rng, lvl):
    start = rng.randrange(0, 12)
    if lvl == "easy":
        steps = [rng.choice([1, 2, 3])] * 5
    elif lvl == "medium":
        a, b = rng.choice([(1, 2), (2, 1), (3, 1), (1, 3), (2, 3)])
        steps = [a, b, a, b, a]
    else:
        s = rng.choice([1, 2])
        steps = [s, s + 1, s + 2, s + 3, s + 4]
    idx = [start]
    for st in steps:
        idx.append(idx[-1] + st)
    R(max(idx) <= 25)
    shown = [chr(65 + i) for i in idx[:5]]
    ans_i = idx[5]
    ans = chr(65 + ans_i)
    gaps = [idx[i + 1] - idx[i] for i in range(4)]
    dist = [chr(65 + ans_i + d) for d in (-2, -1, 1, 2, 3) if 0 <= ans_i + d <= 25]
    return {
        "q": f"Which letter comes next in the series: {', '.join(shown)}, ?",
        "correct": ans,
        "dist": dist,
        "why": (f"Positions (A = 1): {', '.join(str(i + 1) for i in idx[:5])}. Gaps so far: {', '.join(map(str, gaps))}. "
                f"The next gap is {steps[4]}, so the next position is {ans_i + 1}, which is {ans}."),
        "tip": "Convert letters to positions (A = 1) and look at the gaps.",
    }


def p_nseries(rng, lvl):
    if rng.random() < 0.5:
        k = rng.choice([2, 3])
        c = rng.randrange(0, 6)
        x0 = rng.randrange(1, 6)
        s = [x0]
        for _ in range(5):
            s.append(s[-1] * k + c)
        return {
            "q": f"Which number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
            "correct": str(s[5]),
            "dist": [str(s[5] - c), str(s[4] * k + c + 1), str(s[5] + k), str(s[4] + s[3]), str(s[4] + c)],
            "why": f"Each term is the previous term × {k} + {c}. Next: {s[4]} × {k} + {c} = {s[5]}.",
            "tip": "Test the rule on the first two terms before you use it.",
        }
    a = rng.randrange(3, 10)
    x0 = rng.randrange(1, 6)
    s = [x0]
    for i in range(5):
        s.append(s[-1] + a if i % 2 == 0 else s[-1] * 2)
    return {
        "q": f"Which number comes next in the series: {', '.join(map(str, s[:5]))}, ?",
        "correct": str(s[5]),
        "dist": [str(s[4] * 2), str(s[5] + a), str(s[5] * 2), str(s[4] + a + 1), str(s[4] + 2 * a)],
        "why": (f"The rule alternates: add {a}, then multiply by 2. Last step was ×2, so the next step is +{a}: "
                f"{s[4]} + {a} = {s[5]}."),
        "tip": "Look at the first two steps. If they differ, the rule alternates.",
    }


CODE_WORDS = ["RAIN", "TREE", "MANGO", "BIRD", "TRAIN", "PLANT", "LAMP", "SUGAR", "CHAI",
              "DOSA", "MOON", "RIVER", "PEAR", "NEST", "LEAF", "ZONE"]


def _shift(word: str, k: int) -> str:
    return "".join(chr((ord(ch) - 65 + k) % 26 + 65) for ch in word)


def _opp(word: str) -> str:
    return "".join(chr(90 - (ord(ch) - 65)) for ch in word)


def p_code(rng, lvl):
    word = rng.choice(CODE_WORDS)
    kinds = ["shift", "opposite", "digits"] if lvl == "easy" else ["reverse_shift", "opposite", "digits", "shift"]
    kind = rng.choice(kinds)
    if kind == "shift":
        k = rng.randrange(1, 5)
        return {
            "q": f"In a code, each letter is moved {k} place(s) forward in the alphabet (A becomes {chr(65 + k)}). How is the word {word} written in this code?",
            "correct": _shift(word, k),
            "dist": [_shift(word, -k), _shift(word, k + 1), _shift(word, k - 1), _shift(word[::-1], k)],
            "why": f"Move each letter {k} steps forward: " + ", ".join(f"{ch} → {_shift(ch, k)}" for ch in word) + f". Result: {_shift(word, k)}.",
            "tip": "Shifting forward means adding to the letter's position. Wrap Z to A.",
        }
    if kind == "reverse_shift":
        k = rng.randrange(1, 4)
        rev = word[::-1]
        return {
            "q": f"In a code, the word is first written backwards, and then each letter is moved {k} place(s) forward. How is {word} written?",
            "correct": _shift(rev, k),
            "dist": [_shift(word, k), rev, _shift(rev, -k), _shift(word, -k)],
            "why": f"Reverse {word} to get {rev}. Shift each letter {k} forward: {_shift(rev, k)}.",
            "tip": "Do the steps in the order the question gives them.",
        }
    if kind == "opposite":
        return {
            "q": f"In a code, every letter is replaced by its opposite letter (A ↔ Z, B ↔ Y, C ↔ X, and so on). How is {word} written in this code?",
            "correct": _opp(word),
            "dist": [_shift(word, 1), _shift(word, -1), word, _opp(word[::-1])],
            "why": "Opposite of a letter = 25 − its position (A = 0). " + ", ".join(f"{ch} → {_opp(ch)}" for ch in word) + f". Result: {_opp(word)}.",
            "tip": "A is the first letter, so its opposite is Z. The two ends always swap.",
        }
    pos = [ord(ch) - 64 for ch in word]
    return {
        "q": f"In a code, each letter is written as its position in the alphabet (A = 1, B = 2, ..., Z = 26), with hyphens between numbers. What is the code for {word}?",
        "correct": "-".join(map(str, pos)),
        "dist": ["-".join(str(p + 1) for p in pos), "-".join(str(p) for p in reversed(pos)),
                 str(sum(pos)), "-".join(str(p - 1) for p in pos)],
        "why": f"Positions of {word}: " + ", ".join(f"{ch} = {ord(ch) - 64}" for ch in word) + f". Code: {'-'.join(map(str, pos))}.",
        "tip": "Write the position of each letter, then join with hyphens.",
    }


BASE_REL = {
    "father": ("parent", "M"), "mother": ("parent", "F"),
    "son": ("child", "M"), "daughter": ("child", "F"),
    "brother": ("sibling", "M"), "sister": ("sibling", "F"),
    "husband": ("spouse", "M"), "wife": ("spouse", "F"),
}
COMPOSE = {
    ("parent", "sibling"): lambda g: "father" if g == "M" else "mother",
    ("sibling", "parent"): lambda g: "uncle" if g == "M" else "aunt",
    ("child", "sibling"): lambda g: "nephew" if g == "M" else "niece",
    ("child", "parent"): lambda g: "brother" if g == "M" else "sister",
    ("spouse", "child"): lambda g: "son-in-law" if g == "M" else "daughter-in-law",
    ("spouse", "parent"): lambda g: "father" if g == "M" else "mother",
    ("sibling", "sibling"): lambda g: "brother" if g == "M" else "sister",
    ("sibling", "child"): lambda g: "son" if g == "M" else "daughter",
    ("parent", "parent"): lambda g: "grandfather" if g == "M" else "grandmother",
    ("child", "child"): lambda g: "grandson" if g == "M" else "granddaughter",
}
REL_POOL = sorted(set(BASE_REL) | {f(g) for f in COMPOSE.values() for g in "MF"})


def p_blood(rng, lvl):
    X, Y, Z = rng.sample(NAMES, 3)
    l1 = rng.choice(list(BASE_REL))
    l2 = rng.choice(list(BASE_REL))
    k1, g1 = BASE_REL[l1]
    k2, g2 = BASE_REL[l2]
    if k1 == "spouse":
        R(g2 != g1)  # if X is husband of Y, then Y is a wife
    key = (k1, k2)
    R(key in COMPOSE)
    ans = COMPOSE[key](g1)
    return {
        "q": f"{X} is the {l1} of {Y}. {Y} is the {l2} of {Z}. How is {X} related to {Z}?",
        "correct": ans,
        "dist": [r for r in REL_POOL if r != ans],
        "why": (f"Trace the chain: {X} is {Y}'s {l1}, and {Y} is {Z}'s {l2}. "
                f"Combining the two links gives {X} as {Z}'s {ans}."),
        "tip": "Draw the chain on paper. Track the gender of the person you are describing.",
    }


def _seat_holds(c, pos, n):
    kind, a, b = c
    if kind == "left":
        return pos[a] < pos[b]
    if kind == "next":
        return abs(pos[a] - pos[b]) == 1
    if kind == "imm":
        return pos[b] == pos[a] + 1
    if kind == "apart":
        return abs(pos[a] - pos[b]) >= 2
    return pos[a] in (0, n - 1)  # "end"


def _seat_text(c):
    kind, a, b = c
    return {
        "left": f"{a} sits somewhere to the left of {b}.",
        "next": f"{a} sits next to {b}.",
        "imm": f"{a} sits immediately to the left of {b}.",
        "apart": f"{a} does not sit next to {b}.",
        "end": f"{a} sits at one of the two ends.",
    }[kind]


def _seat_count(people, clues, n):
    cnt = 0
    for perm in permutations(people):
        pos = {p: i for i, p in enumerate(perm)}
        if all(_seat_holds(c, pos, n) for c in clues):
            cnt += 1
    return cnt


def p_seating(rng, lvl):
    n = {"easy": 4, "medium": 5, "hard": 6}[lvl]
    people = rng.sample(NAMES, n)
    hidden = people[:]
    rng.shuffle(hidden)
    hpos = {p: i for i, p in enumerate(hidden)}
    pool = [(kind, a, b) for a, b in permutations(people, 2) for kind in ("left", "next", "imm", "apart")]
    pool += [("end", p, None) for p in people]
    pool = [c for c in pool if _seat_holds(c, hpos, n)]
    rng.shuffle(pool)
    clues = []
    cur = _seat_count(people, [], n)
    for c in pool:
        if cur == 1 or len(clues) >= 7:
            break
        trial = clues + [c]
        k = _seat_count(people, trial, n)
        if k < cur:
            clues, cur = trial, k
    R(cur == 1 and len(clues) >= 2)
    sol = next(perm for perm in permutations(people)
               if all(_seat_holds(c, {p: i for i, p in enumerate(perm)}, n) for c in clues))
    kind = rng.choice(["position", "right_of", "count_left"])
    if kind == "position":
        k = rng.randrange(1, n + 1)
        ans = sol[k - 1]
        q = f"Who sits {ORDINALS[k - 1]} from the left?"
        dist = [p for p in people if p != ans]
        why = f"The only seating order from the left is {', '.join(sol)}. {ans} is {ORDINALS[k - 1]} from the left."
    elif kind == "right_of":
        cand = [p for p in people if hpos_sol(sol, p) < n - 1]
        X = rng.choice(cand)
        ans = sol[hpos_sol(sol, X) + 1]
        q = f"Who sits immediately to the right of {X}?"
        dist = [p for p in people if p not in (ans, X)]
        why = f"The only seating order from the left is {', '.join(sol)}. {ans} sits just to the right of {X}."
    else:
        X = rng.choice(people)
        ans_n = hpos_sol(sol, X)
        ans = str(ans_n)
        q = f"How many people sit to the left of {X}?"
        dist = [str(v) for v in (ans_n - 1, ans_n + 1, ans_n + 2, ans_n + 3) if v >= 0]
        why = f"The only seating order from the left is {', '.join(sol)}. {ans_n} {'person' if ans_n == 1 else 'people'} sit to the left of {X}."
    qtext = (f"{n} friends sit in one row, all facing the same way. Seen from the front, the row runs left to right. "
             f"Clues: {' '.join(_seat_text(c) for c in clues)} {q}")
    return {"q": qtext, "correct": ans, "dist": dist, "why": why,
            "tip": "Start with the clue that fixes a person's position, such as an end or an immediate neighbour."}


def hpos_sol(sol, p):
    return sol.index(p)


def _syl_sent(form, x, y, terms):
    X, Y = terms[x], terms[y]
    if form == "all":
        return f"All {X} are {Y}."
    if form == "no":
        return f"No {X} are {Y}."
    if form == "some":
        return f"Some {X} are {Y}."
    return f"Some {X} are not {Y}."


def _syl_holds(form, x, y, m):
    bx, by = 1 << x, 1 << y
    regs = [r for r in range(8) if (m >> r) & 1]
    if form == "all":
        return all(not ((r & bx) and not (r & by)) for r in regs)
    if form == "no":
        return all(not ((r & bx) and (r & by)) for r in regs)
    if form == "some":
        return any((r & bx) and (r & by) for r in regs)
    return any((r & bx) and not (r & by) for r in regs)


def p_syllogism(rng, lvl):
    forms = ("all", "some") if lvl == "easy" else (("all", "some", "no") if lvl == "medium" else ("all", "no", "some", "somenot"))
    terms = rng.sample(["dosas", "sweets", "fruits", "trucks", "students", "doctors", "bikes",
                        "poets", "spices", "bankers", "tigers", "cricketers"], 3)
    stmts = [(f, x, y) for f in forms for x in range(3) for y in range(3) if x != y]
    p1, p2 = rng.sample(stmts, 2)
    R({p1[1], p1[2], p2[1], p2[2]} == {0, 1, 2})

    # Existential import: each category has at least one member
    def _nonempty_model(m):
        regs = [r for r in range(8) if (m >> r) & 1]
        return any(r & 1 for r in regs) and any(r & 2 for r in regs) and any(r & 4 for r in regs)

    models = [m for m in range(256) if _nonempty_model(m) and all(_syl_holds(f, x, y, m) for f, x, y in (p1, p2))]
    R(models)

    # The conclusion must bridge the two end terms through the middle term
    mid = ({p1[1], p1[2]} & {p2[1], p2[2]}).pop()
    end1 = ({p1[1], p1[2]} - {mid}).pop()
    end2 = ({p2[1], p2[2]} - {mid}).pop()

    candidates = [(f, x, y) for f in ("all", "no", "some", "somenot") for (x, y) in ((end1, end2), (end2, end1))]
    entailed = [c for c in candidates if all(_syl_holds(*c, m) for m in models)]
    others = [c for c in candidates if not all(_syl_holds(*c, m) for m in models)]
    R(entailed and len(others) >= 3)

    # Prefer universal statements ('all', 'no') when entailed, otherwise particular ('some', 'somenot')
    universals = [c for c in entailed if c[0] in ("all", "no")]
    correct = rng.choice(universals) if universals else rng.choice(entailed)
    distractors = rng.sample(others, 3)

    return {
        "q": (f"Assume these two statements are true, even if they seem unlikely, and assume each group has at least one member: "
              f"{_syl_sent(*p1, terms)} {_syl_sent(*p2, terms)} Which conclusion must also be true?"),
        "correct": _syl_sent(*correct, terms),
        "dist": [_syl_sent(*c, terms) for c in distractors],
        "why": (f"Both statements together force '{_syl_sent(*correct, terms)}' in every case that fits them. "
                "Each wrong option is false in at least one case that still fits both statements, so it cannot be forced."),
        "tip": "Draw overlapping circles for each statement. Check the conclusion against every possible overlap.",
    }


# ---------------------------------------------------------------- data interpretation

YEARS = ["FY23", "FY24", "FY25"]


def _caselet(rng):
    comps = rng.sample(COMPANIES, rng.choice([3, 4]))
    vals = {c: [rng.randrange(80, 900) for _ in YEARS] for c in comps}
    return comps, vals


def _table(comps, vals):
    head = "| Company (revenue in ₹ lakh) | " + " | ".join(YEARS) + " |"
    sep = "|---|" + "---|" * len(YEARS)
    rows = [f"| {c} | " + " | ".join(str(v) for v in vals[c]) + " |" for c in comps]
    return "\n".join([head, sep, *rows])


def di_avg(rng, lvl):
    comps, vals = _caselet(rng)
    c = rng.choice(comps)
    series = vals[c]
    avg = F(sum(series), 3)
    o = vals[next(x for x in comps if x != c)]
    return {
        "q": (f"The table shows revenue of Indian companies in ₹ lakh.\n\n{_table(comps, vals)}\n\n"
              f"What was the average annual revenue of {c} over FY23 to FY25? Round to one decimal place."),
        "correct": f"₹{dec(avg, 1)} lakh",
        "dist": [f"₹{sum(series)} lakh", f"₹{sorted(series)[1]} lakh", f"₹{max(series)} lakh",
                 f"₹{dec(F(sum(o), 3), 1)} lakh"],
        "why": f"Total of {c} = {' + '.join(map(str, series))} = {sum(series)}. Average = {sum(series)} ÷ 3 = {dec(avg, 1)} lakh.",
        "tip": "Average over three years = total ÷ 3, not the total itself.",
    }


def di_growth(rng, lvl):
    comps, vals = _caselet(rng)
    c = rng.choice(comps)
    ia, ib = sorted(rng.sample(range(3), 2))
    a, b = vals[c][ia], vals[c][ib]
    R(b > a)
    v = F(b - a, a) * 100
    return {
        "q": (f"The table shows revenue of Indian companies in ₹ lakh.\n\n{_table(comps, vals)}\n\n"
              f"What is the percent growth in revenue of {c} from {YEARS[ia]} to {YEARS[ib]}? Round to one decimal place."),
        "correct": f"{dec(v, 1)}%",
        "dist": [f"{dec(F((b - a) * 100, b), 1)}%", f"{dec(F(b, a) * 100, 1)}%", f"₹{b - a} lakh", f"{dec(F(a - b, a) * 100, 1)}%"],
        "why": (f"Growth = (new − old) ÷ old × 100 = ({b} − {a}) ÷ {a} × 100 = {dec(v, 1)}%."),
        "tip": "Always divide by the old value (the base year), not the new one.",
    }


def di_share(rng, lvl):
    comps, vals = _caselet(rng)
    yi = rng.randrange(3)
    c = rng.choice(comps)
    tot = sum(vals[x][yi] for x in comps)
    a = vals[c][yi]
    other = next(x for x in comps if x != c)
    o = vals[other][yi]
    v = F(a * 100, tot)
    return {
        "q": (f"The table shows revenue of Indian companies in ₹ lakh.\n\n{_table(comps, vals)}\n\n"
              f"What share of the total revenue of all companies in {YEARS[yi]} came from {c}? Round to one decimal place."),
        "correct": f"{dec(v, 1)}%",
        "dist": [f"{dec(F(a * 100, tot - a), 1)}%", f"{dec(F(o * 100, tot), 1)}%", f"{dec(F(a, tot), 1)}%", f"{dec(F(tot * 100, a), 1)}%"],
        "why": f"Total in {YEARS[yi]} = {tot}. Share = {a} ÷ {tot} × 100 = {dec(v, 1)}%.",
        "tip": "Share = part ÷ whole × 100. The whole includes every company in the table.",
    }


def di_ratio(rng, lvl):
    comps, vals = _caselet(rng)
    yi = rng.randrange(3)
    c1, c2 = rng.sample(comps, 2)
    a, b = vals[c1][yi], vals[c2][yi]
    R(a != b)
    yj = (yi + 1) % 3
    ca, cb = vals[c1][yj], vals[c2][yj]
    g = gcd(a, b)
    return {
        "q": (f"The table shows revenue of Indian companies in ₹ lakh.\n\n{_table(comps, vals)}\n\n"
              f"What is the ratio of the {YEARS[yi]} revenue of {c1} to that of {c2}? Give the answer in simplest form."),
        "correct": f"{a // g}:{b // g}",
        "dist": [f"{b // g}:{a // g}", f"{a}:{b}", ratio_str(ca, cb), f"{a // g}:{(a + b) // g}"],
        "why": f"{c1} : {c2} = {a} : {b}. Divide both by their HCF {g}: {a // g}:{b // g}.",
        "tip": "Ratios are ordered: the first name goes first. Always reduce by the HCF.",
    }


# ---------------------------------------------------------------- verbal (hand-written, unambiguous)

def fixed(q, correct, dist, why, tip):
    return lambda rng, lvl: {"q": q, "correct": correct, "dist": dist, "why": why, "tip": tip}


VERBAL_PLAN = [
    ("synonyms", fixed("Which word is closest in meaning to FRUGAL?", "Thrifty",
                       ["Generous", "Hungry", "Lazy"],
                       "Frugal and thrifty both mean careful with money. Generous is the opposite.",
                       "Frugal: spends little. Thrifty: spends little."), 1, ("easy",)),
    ("synonyms", fixed("Which word is closest in meaning to CANDID?", "Frank",
                       ["Hidden", "Confused", "Secretive"],
                       "Candid means open and honest in speech. Frank is the closest word.",
                       "Candid and frank both mean open."), 1, ("easy",)),
    ("synonyms", fixed("Which word is closest in meaning to DILIGENT?", "Hard-working",
                       ["Careless", "Cheerful", "Rude"],
                       "A diligent person works with care and effort.",
                       "Diligent = hard-working."), 1, ("easy",)),
    ("synonyms", fixed("Which word is closest in meaning to BENEVOLENT?", "Kind",
                       ["Greedy", "Angry", "Lazy"],
                       "Benevolent means well-meaning and kind. Kind is the closest word.",
                       "Benevolent sounds like 'benefit to others'."), 1, ("easy",)),
    ("synonyms", fixed("Which word is closest in meaning to SCARCE?", "Rare",
                       ["Plentiful", "Cheap", "Colourful"],
                       "Scarce means not easy to find. Rare is the closest word.",
                       "Scarce = few in number."), 1, ("medium",)),
    ("synonyms", fixed("Which word is closest in meaning to RELUCTANT?", "Unwilling",
                       ["Eager", "Quick", "Proud"],
                       "Reluctant means not wanting to do something.",
                       "Reluctant = not keen."), 1, ("medium",)),
    ("synonyms", fixed("Which word is closest in meaning to VERBOSE?", "Wordy",
                       ["Silent", "Tall", "Brief"],
                       "Verbose means using more words than needed.",
                       "Verbose = too many words."), 1, ("medium",)),
    ("synonyms", fixed("Which word is closest in meaning to PRUDENT?", "Wise",
                       ["Reckless", "Famous", "Playful"],
                       "Prudent means careful and sensible about the future.",
                       "Prudent = careful planning."), 1, ("medium",)),
    ("antonyms", fixed("Which word is most nearly the opposite of ANCIENT?", "Modern",
                       ["Old", "Ruined", "Famous"],
                       "Ancient means from a very long time ago. Modern is its opposite.",
                       "Ancient vs modern."), 1, ("easy",)),
    ("antonyms", fixed("Which word is most nearly the opposite of EXPAND?", "Shrink",
                       ["Grow", "Stretch", "Extend"],
                       "Expand means to become larger. Shrink means to become smaller.",
                       "Expand: get bigger. Shrink: get smaller."), 1, ("easy",)),
    ("antonyms", fixed("Which word is most nearly the opposite of ARROGANT?", "Humble",
                       ["Proud", "Bold", "Loud"],
                       "Arrogant means thinking one is better than others. Humble is the opposite.",
                       "Arrogant vs humble."), 1, ("easy",)),
    ("antonyms", fixed("Which word is most nearly the opposite of ABUNDANT?", "Scarce",
                       ["Plenty", "Full", "Rich"],
                       "Abundant means present in large amounts. Scarce means very little.",
                       "Abundant vs scarce."), 1, ("medium",)),
    ("antonyms", fixed("Which word is most nearly the opposite of OPTIMIST?", "Pessimist",
                       ["Realist", "Dreamer", "Critic"],
                       "An optimist expects good outcomes. A pessimist expects bad ones.",
                       "Optimist vs pessimist."), 1, ("medium",)),
    ("antonyms", fixed("Which word is most nearly the opposite of TRANSPARENT?", "Opaque",
                       ["Clear", "Glassy", "Bright"],
                       "Transparent lets light pass through. Opaque does not.",
                       "Opaque = not see-through."), 1, ("medium",)),
    ("grammar", fixed("Choose the correct sentence.", "She has gone to Pune.",
                      ["She has went to Pune.", "She is gone to Pune.", "She have gone to Pune."],
                      "The past participle after 'has' is 'gone'. 'Went' cannot follow 'has'.",
                      "Has + past participle (gone, done, seen)."), 1, ("medium",)),
    ("grammar", fixed("Choose the correct verb: Each of the candidates ___ asked to bring a laptop.", "was",
                      ["were", "are", "have been"],
                      "'Each' is singular, so the verb is singular: 'was asked'.",
                      "Each, every, neither take a singular verb."), 1, ("medium",)),
    ("grammar", fixed("Choose the correct preposition: I am looking forward ___ meeting you.", "to",
                      ["for", "at", "on"],
                      "'Look forward to' is followed by a noun or -ing form, so 'to' is correct.",
                      "Look forward TO doing something."), 1, ("medium",)),
    ("grammar", fixed("Choose the correct spelling.", "Accommodation",
                      ["Accomodation", "Acommodation", "Acomodation"],
                      "Accommodation has two c's and two m's.",
                      "Double c, double m."), 1, ("medium",)),
    ("grammar", fixed("Choose the correct verb: The report, along with the charts, ___ on your desk.", "is",
                      ["are", "have", "were"],
                      "The subject is 'the report'. The phrase 'along with the charts' does not change the verb.",
                      "Ignore phrases that begin with 'along with' or 'together with'."), 1, ("medium",)),
    ("idioms", fixed("What does the idiom 'to break the ice' mean?", "To start a friendly conversation",
                     ["To break something fragile", "To feel very cold", "To end a friendship"],
                     "The idiom means to make people feel comfortable when they first meet.",
                     "Break the ice = start talking."), 1, ("hard",)),
]


# ---------------------------------------------------------------- builder

SECTIONS = [
    ("quant", "Quantitative aptitude", [
        ("percentages", p_percent, 17), ("ratio-proportion", p_ratio, 17), ("averages", p_avg, 17),
        ("profit-loss", p_pl, 17), ("simple-interest", p_si, 17), ("compound-interest", p_ci, 15),
        ("time-work", p_tw, 16), ("time-speed-distance", p_tsd, 16), ("probability", p_prob, 16),
        ("permutations-combinations", p_pc, 16), ("number-series", p_series, 16),
    ]),
    ("logical", "Logical reasoning", [
        ("series-letters", p_letters, 8), ("series-numbers", p_nseries, 7),
        ("coding-decoding", p_code, 12), ("blood-relations", p_blood, 12),
        ("seating-order", p_seating, 12), ("syllogisms", p_syllogism, 9),
    ]),
    ("data-interpretation", "Data interpretation", [
        ("average", di_avg, 15, ("easy",)), ("growth", di_growth, 15, ("medium",)),
        ("share", di_share, 15, ("medium",)), ("ratio", di_ratio, 15, ("hard",)),
    ]),
    ("verbal", "Verbal ability", VERBAL_PLAN),
]


def build(section, label, plan, rng):
    items, expected = [], []
    seen = set()
    k = 0
    for entry in plan:
        topic, fn, count = entry[0], entry[1], entry[2]
        levels = entry[3] if len(entry) > 3 else LEVELS
        for i in range(count):
            lvl = levels[i % len(levels)]
            spec, cands = None, None
            for _ in range(600):
                try:
                    s = fn(rng, lvl)
                except Retry:
                    continue
                if s["q"] in seen:
                    continue
                c = []
                for d in s["dist"]:
                    if d != s["correct"] and d not in c:
                        c.append(d)
                if len(c) < 3:
                    continue
                spec, cands = s, c
                break
            if spec is None:
                raise RuntimeError(f"{section}/{topic} item {i}: no valid generation")
            seen.add(spec["q"])
            wrong = rng.sample(cands, 3)
            pos = k % 4
            k += 1
            opts = wrong[:pos] + [spec["correct"]] + wrong[pos:]
            item = {
                "id": f"apt-{section}-{k:03d}",
                "module": "interview",
                "topic": topic,
                "section": label,
                "difficulty": lvl,
                "question": spec["q"],
                "options": opts,
                "answerIndex": pos,
                "explanation": spec["why"],
            }
            if spec.get("tip"):
                item["shortcut"] = spec["tip"]
            items.append(item)
            expected.append(spec["correct"])
    return items, expected


def self_check(section_items):
    ids = [it["id"] for items, _ in section_items.values() for it in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for sec, (items, expected) in section_items.items():
        for it, exp in zip(items, expected):
            assert it["module"] == "interview"
            assert len(it["options"]) == 4, it["id"]
            assert len(set(it["options"])) == 4, f"{it['id']} options not distinct"
            assert it["options"][it["answerIndex"]] == exp, f"{it['id']} answer mismatch"
            assert it["difficulty"] in LEVELS
        counts = Counter(it["answerIndex"] for it in items)
        assert max(counts.values()) - min(counts.values()) <= 1, f"{sec} answer spread {counts}"


def main() -> None:
    results = {}
    for section, label, plan in SECTIONS:
        rng = random.Random(f"{SEED}:{section}")
        results[section] = build(section, label, plan, rng)
    self_check(results)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for section, (items, _) in results.items():
        path = OUT_DIR / f"aptitude-{section}.json"
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        total += len(items)
        topics = Counter(it["topic"] for it in items)
        print(f"{section}: {len(items)} -> {path.relative_to(ROOT)}")
        for t, c in topics.items():
            print(f"  {t}: {c}")
    print(f"total: {total}")


if __name__ == "__main__":
    main()
