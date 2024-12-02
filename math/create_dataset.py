EXAMPLES = [
    {"answer": 80, "question": "23+57=?", "topic": "Basic Math"},
    {"answer": 96, "question": "12×8=?", "topic": "Basic Math"},
    {
        "answer": 1070,
        "question": "1+100−50+1000−500+25−12+7−3+100000−99999+5000−4500+1−1+1000−999",
        "topic": "Basic Math",
    },
    {
        "answer": 125,
        "question": "10+((10÷(2×3))+(9/(3÷5))×5)÷(1+(2÷2))×3",
        "topic": "Basic Math",
    },
    {"answer": 475423, "question": "(8+5)x36571", "topic": "Basic Math"},
    {"answer": 259259184.2, "question": "3456789123 * 0.075", "topic": "Basic Math"},
    {
        "answer": 12499998914,
        "question": "123456789123456789÷9876543.987654",
        "topic": "Basic Math",
    },
    {
        "answer": 2111.1111,
        "question": "(1234567890 + 876543210) / 1000000",
        "topic": "Basic Math",
    },
    {"answer": 3654320.988, "question": "9876543210 * 0.00037", "topic": "Basic Math"},
    {
        "answer": 247500000,
        "question": "450000000 * 0.23 + 1200000000 * 0.12",
        "topic": "Basic Math",
    },
    {
        "answer": 7720484956,
        "question": "7654321000 * (1 + 0.012) - 3210987000 * 0.008",
        "topic": "Basic Math",
    },
    {
        "answer": 1.752879435,
        "question": "sqrt((4567891234×234567)÷(87654×1234)/0.025)**0.0567",
        "topic": "Basic Math",
    },
    {
        "answer": 1350027028,
        "question": "(9000000000 * 0.15) + (1234567890 / 45678)",
        "topic": "Basic Math",
    },
    {
        "answer": 16,
        "question": "What is the square root of 256?",
        "topic": "Intermediate Math Problems",
    },
    {
        "answer": 256**0.03,
        "question": "256**0.03",
        "topic": "Intermediate Math Problems",
    },
    {
        "answer": 3,
        "question": "Evaluate log10\u200b(1000).",
        "topic": "Intermediate Math Problems",
    },
    {
        "answer": 120,
        "question": "sum of natural numbers from 1 to 15 including 1 and 15",
        "topic": "Intermediate Math Problems",
    },
    {
        "answer": 6,
        "question": "Solve for x: 2x+5=17.",
        "topic": "Intermediate Math Problems",
    },
    {
        "answer": 56,
        "question": "If x=5, evaluate 3x^2−4x+1.",
        "topic": "Intermediate Math Problems",
    },
    {"answer": 1, "question": "Evaluate tan(45∘).", "topic": "Trigonometry"},
    {
        "answer": -1.769551076,
        "question": "log10(|tan(89.99 / 180 * pi) * sin(0.0001/ 180 * pi) - (0.3)^3|)",
        "topic": "Trigonometry",
    },
    {
        "answer": 8.660254038,
        "question": "Find the length of the side opposite a 60° angle in a right triangle where the hypotenuse is 10.",
        "topic": "Trigonometry",
    },
    {
        "answer": 2,
        "question": "cos(pi) + cos(pi) * cos(pi) + cos(pi) * cos(pi) + cos(pi) * cos(pi)",
        "topic": "Trigonometry",
    },
    {
        "answer": -120,
        "question": "Convert -2/3 pi radians into degrees",
        "topic": "Trigonometry",
    },
    {
        "answer": 150,
        "question": "A store sells an item for $120 after a 20% discount. What was the original price? Express the answer in dollars, but do not include the sign.",
        "topic": "Word",
    },
    {
        "answer": 1102.5,
        "question": "A bank account earns 5% annual interest. How much will a $1,000 investment grow to in 2 years, compounded annually? Express the answer in dollars.",
        "topic": "Word",
    },
    {
        "answer": 30000,
        "question": "If a company makes a profit of $200 per unit and sells 150 units, what is the total profit expressed in dollars?",
        "topic": "Word",
    },
    {
        "answer": 191.666666667,
        "question": "Calculate the monthly payment for a $10,000 loan with a 3% annual interest rate over 5 years (simple interest).",
        "topic": "Word",
    },
    {
        "answer": 20,
        "question": "A vehicle travels 300 miles on 15 gallons of fuel. What is the fuel efficiency in miles per gallon?",
        "topic": "Word",
    },
    {
        "answer": 7,
        "question": "Find the derivative of f(x)=x2+3x+2 and evaluate it at x=2.",
        "topic": "Calculus",
    },
    {
        "answer": 12,
        "question": "Compute the definite integral of (3x^2+2x)dx w/ respect to dx from x = 0 to x = 2.",
        "topic": "Calculus",
    },
    {
        "answer": 1,
        "question": "Evaluate dx[e^x* sin(x)]/dx at x=0.",
        "topic": "Calculus",
    },
    {
        "answer": -4,
        "question": "Find the second derivative of f(x)=ln(x) and evaluate it at x=0.5.",
        "topic": "Calculus",
    },
    {
        "answer": 14,
        "question": "Compute ∫(4x−1)dx between x = 1 and x = 3",
        "topic": "Calculus",
    },
]
if __name__ == "__main__":
    from langsmith import Client

    client = Client()
    dataset_name = "Simple Math Problems"

    # Storing inputs in a dataset lets us
    # run chains and LLMs over a shared set of examples.
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Evaluate ability to solve simple math problems.",
    )

    # Prepare inputs, outputs, and metadata for bulk creation
    inputs = [{"question": record["question"]} for record in EXAMPLES]
    outputs = [{"answer": record["answer"]} for record in EXAMPLES]
    metadata = [{"topic": record["topic"]} for record in EXAMPLES]

    client.create_examples(
        inputs=inputs,
        outputs=outputs,
        metadata=metadata,
        dataset_id=dataset.id,
    )
