import { Product } from "@/data/products";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles } from "lucide-react";

interface PerfumeDisplayProps {
  product: Product;
}

export const PerfumeDisplay = ({ product }: PerfumeDisplayProps) => {
  const getMatchColor = (strength: number) => {
    if (strength >= 70) return "bg-gradient-to-r from-green-500 to-emerald-600";
    if (strength >= 50) return "bg-gradient-to-r from-yellow-500 to-amber-600";
    return "bg-gradient-to-r from-orange-500 to-red-600";
  };

  return (
    <Card className="overflow-hidden backdrop-blur-sm bg-card/95 border-2 shadow-2xl animate-in fade-in-50 slide-in-from-bottom-4 duration-500">
      <div className="bg-gradient-to-br from-primary/10 via-accent/5 to-transparent p-8">
        <div className="flex items-center gap-2 mb-6">
          <Sparkles className="w-5 h-5 text-accent" />
          <h2 className="text-2xl font-bold text-foreground">Your Perfect Match</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Perfume Image */}
          <div className="relative">
            <div className="aspect-square rounded-xl overflow-hidden bg-background shadow-lg ring-1 ring-border">
              <img
                src={product.perfumeImage}
                alt={product.perfumeName}
                className="w-full h-full object-contain p-4"
              />
            </div>
            <div className="absolute -top-3 -right-3">
              <Badge className="text-lg px-4 py-2 shadow-lg bg-gradient-to-r from-accent to-secondary border-0">
                {product.matchStrength}% Match
              </Badge>
            </div>
          </div>

          {/* Perfume Details */}
          <div className="flex flex-col justify-center space-y-6">
            <div>
              <h3 className="text-3xl font-bold text-foreground mb-2">
                {product.perfumeName}
              </h3>
              <p className="text-lg text-muted-foreground italic">
                {product.perfumeBrand}
              </p>
            </div>

            {/* Match Strength Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Match Strength</span>
                <span className="font-semibold">{product.matchStrength}%</span>
              </div>
              <div className="h-3 bg-muted rounded-full overflow-hidden">
                <div
                  className={`h-full ${getMatchColor(product.matchStrength)} transition-all duration-1000 ease-out`}
                  style={{ width: `${product.matchStrength}%` }}
                />
              </div>
            </div>

            {/* Scent Notes */}
            <div className="space-y-2">
              <h4 className="font-semibold text-foreground">Scent Profile</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {product.perfumeNotes}
              </p>
            </div>

            {/* Matched Notes */}
            <div className="space-y-2">
              <h4 className="font-semibold text-foreground">Why It Matches</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {product.reasoning}
              </p>
              <div className="flex flex-wrap gap-2 mt-2">
                {product.matchedNotes.split(',').map((note, index) => (
                  <Badge key={index} variant="secondary" className="text-xs">
                    {note.trim()}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
