import { useState, useEffect } from "react";
import scrapedData from "./data/product_data.json";

function App() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Load the data
    try {
      console.log("Loading data...");
      setProducts(scrapedData);
      
      // Extract unique categories
      const uniqueCategories = ['All', ...new Set(scrapedData.map(item => item.category))];
      setCategories(uniqueCategories);
      
      // Initialize filtered products with all products
      setFilteredProducts(scrapedData);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  }, []);

  // Filter products when category or search term changes
  useEffect(() => {
    let results = [...products];
    
    // Filter by category if not "All"
    if (selectedCategory !== 'All') {
      results = results.filter(product => product.category === selectedCategory);
    }
    
    // Filter by search term
    if (searchTerm) {
      results = results.filter(product => 
        product.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredProducts(results);
  }, [selectedCategory, searchTerm, products]);

  // Simple star rating display without using StarIcon
  const renderRating = (rating) => {
    return (
      <div className="flex items-center">
        <span className="text-yellow-500">
          {"★".repeat(Math.round(rating))}
          {"☆".repeat(5 - Math.round(rating))}
        </span>
        <span className="ml-1 text-gray-600">({rating.toFixed(1)})</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
          Product Catalog
        </h1>
        
        {/* Search and filter controls */}
        <div className="mb-8 flex flex-col sm:flex-row gap-4">
          <div className="w-full sm:w-1/2">
            <input
              type="text"
              placeholder="Search products..."
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="w-full sm:w-1/2">
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Results count */}
        <p className="text-gray-600 mb-4">
          Showing {filteredProducts.length} products
          {selectedCategory !== 'All' ? ` in ${selectedCategory}` : ''}
          {searchTerm ? ` matching "${searchTerm}"` : ''}
        </p>
        
        {/* Product grid */}
        {filteredProducts.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                <div className="p-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">{product.name}</h3>
                  <p className="text-xl font-bold text-green-600 mb-2">{product.price}</p>
                  <div className="mb-4">
                    {renderRating(product.rating)}
                  </div>
                  <div className="mt-4">
                    <a 
                      href={product.link} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors duration-300"
                    >
                      View Product
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-lg text-gray-600">No products found matching your criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;