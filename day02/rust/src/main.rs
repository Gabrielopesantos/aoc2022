use std::collections::HashMap;

fn get_hashmap() -> HashMap<&'static str, i32> {
    let mut map = HashMap::new();

    map.insert("A X", 1 + 3);
    map.insert("A Y", 2 + 6);
    map.insert("A Z", 3 + 0);
    map.insert("B X", 1 + 0);
    map.insert("B Y", 2 + 3);
    map.insert("B Z", 3 + 6);
    map.insert("C X", 1 + 6);
    map.insert("C Y", 2 + 0);
    map.insert("C Z", 3 + 3);

    return map;
}

fn get_hashmap_pt2() -> HashMap<&'static str, i32> {
    let mut map = HashMap::new();

    map.insert("A X", 3 + 0);
    map.insert("A Y", 1 + 3);
    map.insert("A Z", 2 + 6);
    map.insert("B X", 1 + 0);
    map.insert("B Y", 2 + 3);
    map.insert("B Z", 3 + 6);
    map.insert("C X", 2 + 0);
    map.insert("C Y", 3 + 3);
    map.insert("C Z", 1 + 6);

    return map;
}

fn main() {
    // std::fs:read_to_string / unwrap()
    let rounds: Vec<&str> = include_str!("../../input.txt").lines().collect();

    let game_outcomes = get_hashmap();

    let mut sum = 0;
    for r in rounds.iter() {
        if let Some(score) = game_outcomes.get(r) {
            sum += score;
        }
    }

    let game_outcomes_pt2 = get_hashmap_pt2();

    println!("Part 1: {}", sum);

    let mut sum = 0;
    for r in rounds {
        if let Some(score) = game_outcomes_pt2.get(r) {
            sum += score;
        }
    }

    println!("Part 2: {}", sum);
}
