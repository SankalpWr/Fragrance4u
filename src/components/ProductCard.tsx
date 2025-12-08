import { Product } from "@/data/products";
import { Card } from "@/components/ui/card";

interface ProductCardProps {
  product: Product;
  isSelected: boolean;
  onClick: () => void;
}

export const ProductCard = ({ product, isSelected, onClick }: ProductCardProps) => {
  return (
    <Card
      onClick={onClick}
      className={`group cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-xl ${
        isSelected ? "ring-2 ring-primary shadow-xl scale-[1.02]" : ""
      }`}
    >
      <div className="aspect-square overflow-hidden bg-muted">
        <img
          src={product.bodywashImage}
          alt="Body wash product"
          className="w-full h-full object-contain transition-transform duration-500 group-hover:scale-110"
          loading="lazy"
        />
      </div>
      <div className="p-4 bg-card">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {product.bodywashNotes}
        </p>
      </div>
    </Card>
  );
};
