import { Leaf } from 'lucide-react';

export default function Logo({ size = 'md', showText = true }) {
  const sizes = {
    sm: { icon: 20, text: 'text-base' },
    md: { icon: 28, text: 'text-xl' },
    lg: { icon: 36, text: 'text-2xl' },
  };
  const s = sizes[size] || sizes.md;

  return (
    <div className="flex items-center gap-2">
      <div className="bg-primary-700 p-2 rounded-xl shadow-md flex items-center justify-center">
        <Leaf size={s.icon} className="text-white" />
      </div>
      {showText && (
        <div>
          <div className={`font-bold text-primary-900 leading-tight ${s.text}`}>
            CropSense AI
          </div>
          <div className="text-xs text-primary-600 font-medium leading-tight hidden sm:block">
            Disease Knowledge Assistant
          </div>
        </div>
      )}
    </div>
  );
}

