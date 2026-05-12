from openai import OpenAI
import tiktoken
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

PROMPT = "Suggest a creative name for a mobile app that helps people find hiking trails."
MODEL = "gpt-4o-mini"
TEMPERATURES = [0, 0.3, 0.7, 1.0, 1.5]
RUNS_PER_TEMP = 10


def generate_outputs(prompt: str, temperature: float, n_runs: int) -> list[str]:
    """Generate multiple outputs at a given temperature."""
    outputs = []
    for _ in range(n_runs):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=100,
        )
        outputs.append(response.choices[0].message.content.strip())
    return outputs


def calculate_diversity(outputs: list[str]) -> dict:
    """Calculate diversity metrics for a set of outputs."""
    unique_outputs = set(outputs)
    # Unique words across all outputs
    all_words = " ".join(outputs).lower().split()
    unique_words = set(all_words)

    return {
        "total_outputs": len(outputs),
        "unique_outputs": len(unique_outputs),
        "uniqueness_ratio": len(unique_outputs) / len(outputs),
        "total_words": len(all_words),
        "unique_words": len(unique_words),
        "vocabulary_diversity": len(unique_words) / len(all_words) if all_words else 0,
    }


# Run the experiment
print(f"Prompt: {PROMPT}")
print(f"Runs per temperature: {RUNS_PER_TEMP}")
print("=" * 70)

results = {}

for temp in TEMPERATURES:
    print(f"\nTemperature: {temp}")
    print("-" * 40)

    outputs = generate_outputs(PROMPT, temp, RUNS_PER_TEMP)
    metrics = calculate_diversity(outputs)
    results[temp] = metrics

    # Print sample outputs
    for i, output in enumerate(outputs[:3]):
        print(f"  Sample {i+1}: {output[:80]}...")

    print(f"\n  Unique outputs: {metrics['unique_outputs']}/{metrics['total_outputs']}")
    print(f"  Uniqueness ratio: {metrics['uniqueness_ratio']:.2f}")
    print(f"  Vocabulary diversity: {metrics['vocabulary_diversity']:.2f}")

# Summary table
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"{'Temperature':<15}{'Unique Outputs':<20}{'Uniqueness %':<18}{'Vocab Diversity'}")
print("-" * 70)

for temp in TEMPERATURES:
    m = results[temp]
    print(
        f"{temp:<15}"
        f"{m['unique_outputs']}/{m['total_outputs']:<17}"
        f"{m['uniqueness_ratio']:.0%}{'':<14}"
        f"{m['vocabulary_diversity']:.2%}"
    )