def square(x):
    return x+x

operation = square
print(operation(5))

def apply_to_list(func, items):
    return [func(item,item+1) for item in items]

scores = [0.8, 0.3, 0.95, 0.4]
normalized = apply_to_list(lambda x,y: round(x*10*y), scores)
print(normalized)

def by_accuracy(result):
    return result["accuracy"]

def by_latency(result):
    return result["latency_ms"]

results = [
    {"model": "large-resoning-model", "accuracy": 0.92,
     "latency_ms": 800},
    {"model": "balanced model", "accuracy": 0.95,
     "latency_ms": 1200},
    {"model": "small-local-model", "accuracy": 0.88,
     "latency_ms": 200}
]

fastest = sorted(results, key = by_latency,)
print(fastest)
most_accurate  = sorted(results, key = by_accuracy, reverse = True)
print(most_accurate)


# *args and **kwargs are common in AI codebases.
# espeically in wrapper functions that forward arguments to provider SDKs,
# model client s or shared utility functions

# *args collects positional arguments into a tuple, **kwargs collects keyword arguments into a dictionary.

def log_and_call(func, *args, **kwargs):
    print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
    return func(*args,**kwargs)

def embed_text(text, model="text-embedding-3-small", dimensions = 256):
    return f"Embedding '{text}' with {model} ({dimensions}d)"

result = log_and_call(embed_text, "hello world", model="text-embedding-3-large")
print(result)

def call_llm(prompt, **kwargs):
    """Set project defaults while allowing each call to override them"""
    defaults = {
        "model": "fast-default-model",
        "temperature": 0.2,
        "max_output_tokens": 1000
    }
    config = {**defaults, **kwargs} # this merges two dictionaries. the later value overrides earlier ones.
    print(f"Calling {config['model']} with temp = {config['temperature']}")
    return config

call_llm("Explain RAG")
call_llm("Explain RAG", temperature = 0.0, max_output_tokens = 500)

#Closures
def make_multiplier(factor):
    def multiply(x):
        return x*factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
#When make_multiplier(2) runs, it creates the inner multiply functions and returns it.
# the returned function still has access to factor =2.

print(double(10))
print(triple(10))

def make_classifier(threshold):
    def classify(score):
        return "positive" if score >= threshold else "negative"
    return classify

strict = make_classifier(0.9)
lenient = make_classifier(0.5)
scores = [0.45, 0.92, 0.5, 0.88]
print([strict(s) for s in scores])
print([lenient(s) for s in scores])


        