use std::collections::HashSet;

fn main() {
    let rucksacks: Vec<(&str, &str)> = include_str!("../../input.txt")
        .lines()
        .map(|x| {
            let half_len = x.len() / 2;
            x.split_at(half_len)
        })
        .collect();

    let mut priority_sum: i32 = 0;
    for (first_sack, second_sack) in &rucksacks {
        // chars
        let f_sack_hs: HashSet<char> = first_sack.chars().into_iter().collect();
        let s_sack_hs: HashSet<char> = second_sack.chars().into_iter().collect();

        // Bytes
        //let f_sack_hs: HashSet<u8> = first_sack.as_bytes().to_vec().into_iter().collect();
        //let s_sack_hs: HashSet<u8> = second_sack.as_bytes().to_vec().into_iter().collect();
        let common = f_sack_hs.intersection(&s_sack_hs).collect::<Vec<&char>>()[0];

        if *common >= 'a' {
            priority_sum += (*common as u8 - 'a' as u8 + 1) as i32;
        } else {
            priority_sum += (*common as u8 - 'A' as u8 + 27) as i32;
        }
    }

    println!("Part 1: {:?}", priority_sum);

    let mut group = 1;
    let mut group_sacks: Vec<HashSet<char>> = vec![];
    let mut priority_sum_badges: i32 = 0;
    for (first_sack, second_sack) in rucksacks {
        // chars
        let sack_hs: HashSet<char> = HashSet::from_iter(
            [first_sack, second_sack]
                .join("")
                .chars()
                .into_iter()
                .collect::<HashSet<char>>(),
        );
        group_sacks.push(sack_hs);

        if group == 3 {
            let intersection: HashSet<char> = HashSet::from_iter(
                group_sacks[0]
                    .intersection(&group_sacks[1])
                    .map(|x| *x) // ?
                    .collect::<HashSet<char>>(),
            );
            let common = intersection
                .intersection(&group_sacks[2])
                .collect::<Vec<&char>>()[0];

            if *common >= 'a' {
                priority_sum_badges += (*common as u8 - 'a' as u8 + 1) as i32;
            } else {
                priority_sum_badges += (*common as u8 - 'A' as u8 + 27) as i32;
            }

            group = 0;
            group_sacks.clear();
        }

        group += 1;
    }
    println!("Part 2: {:?}", priority_sum_badges);
}
