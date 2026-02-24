import Image from "next/image";

export function BrandMark() {
  return (
    <div className="flex items-center gap-3">
      <Image
        src="/stone_icon.jpg"
        alt="Stone AI"
        width={40}
        height={40}
        className="h-10 w-10 rounded-lg shadow-sm"
      />
      <div className="leading-tight">
        <div className="font-heading text-sm uppercase tracking-[0.26em] text-strong">
          STONE AI
        </div>
        <div className="text-[11px] font-medium text-quiet">
          Mission Control
        </div>
      </div>
    </div>
  );
}
