use std::io::{self, BufRead, BufReader, Result};
use std::fs::File;

struct Point (usize, usize);

fn parse_input(filename: &str) -> Result<()> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut each_line = reader.lines();
    let start_point_line = each_line.next().unwrap()?;
    let end_point_line = each_line.next().unwrap()?;

    println!("--------------");
    println!("{} : {}", start_point_line, end_point_line);
    println!("{:?}", parse_point(&start_point_line));
    println!("{:?}", parse_point(&end_point_line));
    Ok(())
}

fn parse_point(point_line: &str) -> Result<()> {
    let coordinate: Vec<_> = 
        point_line.split(|c: char| c == '(' || c == ')' || c == ',')
        .collect();
    println!("Coordinate: {:?}", coordinate);
    Ok(())
}

fn main() -> Result<()> {
    // let (maze, start, goal) = parse_input("../../input.txt")?;
    parse_input("../input.txt");
    Ok(())
}