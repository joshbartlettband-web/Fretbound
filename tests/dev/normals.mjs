// Normal maps for the hang sheets (art/hang/*_hang.png), made with claude-pxl's bump() (github.com/augusto-scarvalho/claude-pxl, MIT).
//   PXL=/path/to/claude-pxl node tests/dev/normals.mjs OUT_DIR [id ...]   -> OUT_DIR/<id>_<dome|luma|mix>.png
// dome: each figure bulges like a pillow from its outline; luma: height from the painting's own shading; mix: the two added.
// Encoding as claude-pxl writes it (and Godot, Unity): RGB = normal * 0.5 + 0.5, green pointing up, (128,128,255) facing us.
import fs from "fs"; import path from "path";
const PXL = process.env.PXL || "/home/user/augusto-scarvalho/claude-pxl";
const { decodePng, encodePng } = await import(path.join(PXL, "src/node/png.ts"));
const { bump, normalImage } = await import(path.join(PXL, "src/core/normals.ts"));
const [out, ...ids] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const dir = new URL("../../art/hang/", import.meta.url).pathname;
const list = ids.length ? ids : fs.readdirSync(dir).filter((f) => f.endsWith("_hang.png")).map((f) => f.slice(0, -9));
for (const id of list) {
  const src = decodePng(fs.readFileSync(path.join(dir, id + "_hang.png")));
  const mask = new Uint8Array(src.w * src.h); for (let i = 0; i < mask.length; i++) mask[i] = (src.data[i] & 255) > 127 ? 1 : 0;
  const make = (o) => { const im = decodePng(fs.readFileSync(path.join(dir, id + "_hang.png"))); im.norm = undefined; bump(im, mask, o); return im; };
  const dome = make({ shape: "dome", depth: 1 }), luma = make({ shape: "luma", depth: 2.5 });
  const mix = make({ shape: "dome", depth: 1 }), a = dome.norm, b = luma.norm, m = mix.norm;
  for (let i = 0; i < mask.length; i++) { if (!mask[i]) continue;
    const x = a[i * 3] + b[i * 3], y = a[i * 3 + 1] + b[i * 3 + 1], z = a[i * 3 + 2] + b[i * 3 + 2], l = Math.hypot(x, y, z) || 1;
    m[i * 3] = Math.round(x / l * 127); m[i * 3 + 1] = Math.round(y / l * 127); m[i * 3 + 2] = Math.max(1, Math.round(z / l * 127)); }
  for (const [k, im] of [["dome", dome], ["luma", luma], ["mix", mix]]) fs.writeFileSync(path.join(out, `${id}_${k}.png`), encodePng(normalImage(im)));
  console.log(id, src.w + "x" + src.h);
}
