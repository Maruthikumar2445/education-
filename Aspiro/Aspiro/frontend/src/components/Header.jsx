export default function Header() {
    return (
      <header className="p-4">
        <div className="flex items-center gap-2">
          <img src="images/aspiro-icon.png" alt="Aspiro" className="h-8" />
          <h1 className="text-2xl font-bold">ASPIRO</h1>
        </div>
        <p className="mt-2 text-lg text-gray-600">
          Transforming education, making learning engaging and inclusive.
        </p>
      </header>
    );
  }