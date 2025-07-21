import { Link } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="py-6 px-8">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center gap-2">
          <img src="images/aspiro-icon.png" alt="Aspiro Logo" className="h-8" />
          <span className="text-white text-2xl font-semibold">ASPIRO</span>
        </Link>
        
        <div className="flex items-center gap-8">
          <Link to="/" className="text-white hover:text-gray-200 transition-colors">
            Home
          </Link>
          <Link to="/about" className="text-white hover:text-gray-200 transition-colors">
            About us
          </Link>
          <Link to="/features" className="text-white hover:text-gray-200 transition-colors">
            Features
          </Link>
          <Link to="/signup">
          <button className="bg-transparent text-white px-6 py-2 rounded-full border-4 border-white hover:bg-white hover:text-indigo-900 transition-all duration-300 transform hover:scale-105">
                signup / login
            </button>
          </Link>
          
        </div>
      </div>
    </nav>
  )
}

export default Navbar