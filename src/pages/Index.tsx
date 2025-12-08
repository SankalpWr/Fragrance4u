import { useState, useMemo } from "react";
import { products } from "@/data/products";
import { ProductCard } from "@/components/ProductCard";
import { PerfumeDisplay } from "@/components/PerfumeDisplay";
import { SearchBar } from "@/components/SearchBar";
import { Button } from "@/components/ui/button";
import { Sparkles } from "lucide-react";

type GenderFilter = "All" | "Men" | "Women" | "Unisex";

const Index = () => {
  const [selectedProduct, setSelectedProduct] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [genderFilter, setGenderFilter] = useState<GenderFilter>("All");

  const filteredProducts = useMemo(() => {
    let filtered = products;
    
    // Apply gender filter
    if (genderFilter !== "All") {
      filtered = filtered.filter(product => 
        product.gender.toLowerCase() === genderFilter.toLowerCase()
      );
    }
    
    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(product => 
        product.bodywashNotes.toLowerCase().includes(query) ||
        product.perfumeName.toLowerCase().includes(query) ||
        product.perfumeBrand.toLowerCase().includes(query) ||
        product.perfumeNotes?.toLowerCase().includes(query) ||
        product.gender.toLowerCase().includes(query)
      );
    }
    
    return filtered;
  }, [searchQuery, genderFilter]);

  const handleProductSelect = (id: number) => {
    setSelectedProduct(id);
    // Smooth scroll to results
    setTimeout(() => {
      document.getElementById("perfume-result")?.scrollIntoView({ 
        behavior: "smooth",
        block: "start"
      });
    }, 100);
  };

  const selected = products.find(p => p.id === selectedProduct);

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-muted/30 to-background">
      {/* Hero Section */}
      <header className="container mx-auto px-4 py-16 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/20 mb-6 animate-in fade-in slide-in-from-top-4 duration-700">
          <Sparkles className="w-4 h-4 text-accent" />
          <span className="text-sm font-medium text-accent">Scent Matching Technology</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent animate-in fade-in slide-in-from-top-6 duration-700 delay-150">
          Find Your Signature Scent
        </h1>
        
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto animate-in fade-in slide-in-from-top-8 duration-700 delay-300">
          Discover the perfect perfume match for your favorite body wash. 
          Our algorithm analyzes scent profiles to find your ideal fragrance pairing.
        </p>
      </header>

      {/* Search Bar */}
      <section className="container mx-auto px-4 pb-4">
        <SearchBar value={searchQuery} onChange={setSearchQuery} />
      </section>

      {/* Gender Filter */}
      <section className="container mx-auto px-4 pb-8">
        <div className="flex flex-wrap justify-center gap-2">
          {(["All", "Men", "Women", "Unisex"] as GenderFilter[]).map((gender) => (
            <Button
              key={gender}
              variant={genderFilter === gender ? "default" : "outline"}
              size="sm"
              onClick={() => setGenderFilter(gender)}
              className="min-w-[80px]"
            >
              {gender}
            </Button>
          ))}
        </div>
        {(searchQuery || genderFilter !== "All") && (
          <p className="text-center text-sm text-muted-foreground mt-4">
            Found {filteredProducts.length} product{filteredProducts.length !== 1 ? 's' : ''}
          </p>
        )}
      </section>

      {/* Product Grid */}
      <section className="container mx-auto px-4 pb-16">
        <h2 className="text-3xl font-bold mb-8 text-center text-foreground">
          Select Your Body Wash
        </h2>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 md:gap-6">
          {filteredProducts.map((product, index) => (
            <div 
              key={product.id}
              className="animate-in fade-in slide-in-from-bottom-4 duration-500"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <ProductCard
                product={product}
                isSelected={selectedProduct === product.id}
                onClick={() => handleProductSelect(product.id)}
              />
            </div>
          ))}
        </div>
      </section>

      {/* Perfume Display */}
      {selected && (
        <section id="perfume-result" className="container mx-auto px-4 pb-24">
          <PerfumeDisplay product={selected} />
        </section>
      )}

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8 text-center text-sm text-muted-foreground">
          <p>Personalized scent recommendations powered by fragrance note analysis</p>
        </div>
      </footer>
    </main>
  );
};

export default Index;
