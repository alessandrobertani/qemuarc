from bop import Bop
from argparse import ArgumentParser
from pathlib import Path
from json import dump

def parse_args():
    parser = ArgumentParser(description='Bop')
    parser.add_argument("-i", "--input", help="input file or path", required=True)
    parser.add_argument("-o", "--output", help="directory for any output files", required=False)
    parser.add_argument("-x", "--extract", action="store_true", default=False, help="extract main firmware", required=False)

    args = parser.parse_args()
    return args

def extract_main_fw(bop: Bop, output_dir: Path, extract: bool):
    main_fw = bop.binary_data.packages[3].binary_data.bin_data
    num_package = 0
    for fw in main_fw[:-1]:
        if extract:
            fpath = output_dir.joinpath(f"fw_image_{num_package}.bin")
            with open(fpath, "wb") as f:
                f.write(fw.binary)

        metadata = {}
        metadata["proc"] = fw.img.magic.decode()
        num_block = 0
        for blk in fw.blk:
            blk_data = {}
            blk_data["dst"] = blk.dst
            blk_data["src"] = blk.src - 12 - 12 * len(fw.blk)
            blk_data["blk_size"] = blk.blk_size
            metadata[f"block_{num_block}"] = blk_data
            num_block += 1

        jpath = output_dir.joinpath(f"fw_image_{num_package}.json")
        with open(jpath, "w") as f:
            dump(metadata, f, indent=4)
        
        num_package += 1

def main():
    args = parse_args()

    input = Path(args.input)
    if args.output:
        outdir = Path(args.output)
    else:
        outdir = Path.cwd()

    if args.extract:
        extract = True
    else:
        extract = False

    if not outdir.exists():
        outdir.mkdir(parents=True)
    
    b = Bop.from_file(input)

    
    extract_main_fw(b, outdir, extract)



if __name__ == '__main__':
    main()