fn main() {
    let mut lines_parse: Vec<u32> = include_str!("../../input.txt")
        .split("\n\n")
        .map(|line| line.split("\n").flat_map(|num| num.parse::<u32>()).sum())
        .collect();

    lines_parse.sort_by(|a, b| b.cmp(a));

    println!("Part 1: {:?}", lines_parse[0]);
    println!("Part 2: {}", lines_parse.into_iter().take(3).sum::<u32>());
}
