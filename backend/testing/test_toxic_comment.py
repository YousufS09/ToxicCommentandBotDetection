import joblib

PIPE_PATH = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentandBotDetection\Models\TFIDF\tfidf_pipeline.joblib"

def load_pipeline():
    pipe = joblib.load(PIPE_PATH)
    return pipe

def main():
    pipe = load_pipeline()

    print("\n=== TOXIC COMMENT TESTING ===")
    print("Type a tweet/comment to test it.")
    print("Type 'exit' to quit.\n")

    while True:
        text = input("Enter a tweet/comment: ")

        if text.lower().strip() == "exit":
            print("Exiting...")
            break

        if not text.strip():
            print("Empty input, please type something.\n")
            continue

        pred = pipe.predict([text])[0]
        prob = pipe.predict_proba([text])[0][1]

        print("\n--- RESULT ---")
        print("Comment:", text)
        print("Prediction (0 = Not Toxic, 1 = Toxic):", pred)
        print("Toxicity Probability:", round(float(prob), 4), "\n")

if __name__ == "__main__":
    main()
