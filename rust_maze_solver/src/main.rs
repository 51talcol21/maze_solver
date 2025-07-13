use std::io::{self, BufRead, BufReader, Result};
use std::fs::File;

#[derive(Debug)]
struct Point (usize, usize);

fn parse_input(filename: &str) -> Result<(Vec<Vec<u8>>, Point, Point)> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut all_lines = reader.lines();
    let start_point_line = all_lines.next().unwrap()?;
    let end_point_line = all_lines.next().unwrap()?;

    let start_point = parse_point(&start_point_line);
    let end_point = parse_point(&end_point_line);

    let mut maze = Vec::<Vec<u8>>::new();

    for each_line in all_lines {
        let row = each_line?.split_whitespace()
            .filter(|s| s.chars().all(char::is_numeric))
            .map(|s| s.parse::<u8>().unwrap())
            .collect::<Vec<u8>>();
        println!("{:?}", row);
        maze.push(row);
    }
    Ok((maze, start_point.unwrap(), end_point.unwrap()))
}

fn parse_point(point_line: &str) -> Result<(Point)> {
    let coordinate: Vec<_> = 
        point_line.split(|c: char| c == '(' || c == ')' || c == ',')
        .filter(|s| !s.is_empty() && s.chars().all(char::is_numeric))
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    Ok(Point (coordinate[0], coordinate[1]))
}

fn main() -> Result<()> {
    let (maze, start_point, end_point) = parse_input("../input.txt").unwrap();
    println!("{:?} : {:?} : {:?}", maze, start_point, end_point);
    Ok(())
}