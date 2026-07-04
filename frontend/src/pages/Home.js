function Home() {
  return (
    <div>
      <h2>Welcome</h2>

      <p>
        This application analyzes social media activity to identify
        <strong> toxic comments </strong>
        and detect
        <strong> bot accounts </strong>
        using machine learning models.
      </p>

      <section>
        <h3>What can you do?</h3>
        <ul>
          <li>Analyze text to check if a comment is toxic</li>
          <li>Detect whether a user account behaves like a bot</li>
          <li>Perform a combined risk analysis</li>
        </ul>
      </section>

      <section>
        <h3>Get Started</h3>
        <p>
          Use the navigation bar above to explore the features.
        </p>
      </section>
    </div>
  );
}

export default Home;
