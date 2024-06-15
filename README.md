# VeraCryptPassTester

**VeraCryptPassTester** is a Python script that generates and tests multiple password combinations for VeraCrypt containers. It utilizes various operations like permutations and power sets to create comprehensive password lists and tests them to find the correct one efficiently.

## Features
- Generate password combinations using permutations, exact matches, one-of options, and power sets.
- Test each combination on a VeraCrypt container.
- Display dynamic progress updates with estimated remaining time.

## Usage

1. **Clone the repository:**
    ```bash
    git clone https://github.com/tovam/VeraCryptPassTester.git
    cd VeraCryptPassTester
    ```

2. **Install required dependencies:**
    Ensure you have `veracrypt` installed on your system.

3. **Run the script:**
    ```bash
    python veracrypt_pass_tester.py /path/to/veracrypt/container
    ```

4. **Input password elements:**
    Enter elements for the password template in the following format:
    - `perms(a,b,c)` for permutations
    - `exact(a,b,c)` for exact matches
    - `oneof(a,b,c)` for one-of options
    - `power(a,b,c)` for power sets

    Press Enter after each element input. When finished, press Enter without any input.

Sure, here's the updated example section with the complete list of combinations for the operations `perms`, `oneof`, and `power`.

## Example

```bash
python veracrypt_pass_tester.py /path/to/veracrypt/container
```

Input password elements as prompted:
```
Enter elements (hidden input):
 > perms(aA,bB)
 > oneof(1,2,3)
 > power(xx,yy)
 > 
```

This will generate combinations such as:

- `aAbB1`
- `aAbB2`
- `aAbB3`
- `bBaA1`
- `bBaA2`
- ...
- `bBaA3yy`
- `bBaA3xxyy`

These combinations are generated using:
- `perms(aA,bB)`: `aAbB`, `bBaA`
- `oneof(1,2,3)`: `1`, `2`, `3`
- `power(x,y)`: ` `, `xx`, `yy`, `xxyy`

Each combination is tested on the specified VeraCrypt container.

## Contributing

Contributions are welcome, please fork the repository and submit a pull request.
