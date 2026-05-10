"""
Banquet Logic Puzzle - Final Solution
Problem: Circular table, each person says "both neighbors are liars"
         Lady says "11 people", Gentleman says "She lies, it's 10 people"
         Some always tell truth, others always lie completely.
         Find the number of people.
"""

from itertools import product

def check_arrangement(arr):
    """Verify: each person's statement matches their type"""
    n = len(arr)
    for i in range(n):
        left = (i - 1) % n
        right = (i + 1) % n
        # Person i claims: both neighbors are liars (F)
        statement = (not arr[left]) and (not arr[right])
        # Truth-teller's statement must be true, liar's must be false
        if arr[i] != statement:
            return False
    return True

def has_both_types(arr):
    """Verify: both truth-tellers and liars exist"""
    return 0 < sum(arr) < len(arr)

def find_valid_scenarios(n, lady_type, gent_type):
    """Find all valid arrangements for given n and speaker types"""
    valid = []
    for arr in product([True, False], repeat=n):
        if not check_arrangement(arr) or not has_both_types(arr):
            continue
        
        # Check all adjacent (Lady, Gent) positions
        for lady_pos in range(n):
            gent_pos = (lady_pos + 1) % n
            
            # Verify Lady's statement: "11 people"
            lady_claim_true = (n == 11)
            lady_ok = (arr[lady_pos] == lady_type) and (arr[lady_pos] == lady_claim_true)
            
            # Verify Gent's statement: "Lady lies AND it's 10"
            gent_part1 = (arr[lady_pos] == False)  # "Lady lies"
            gent_part2 = (n == 10)                  # "It's 10"
            gent_statement_true = gent_part1 and gent_part2
            gent_ok = (arr[gent_pos] == gent_type) and (arr[gent_pos] == gent_statement_true)
            
            if lady_ok and gent_ok:
                valid.append((arr, lady_pos, gent_pos))
    return valid

def analyze_neighbor_uniformity(n):
    """Analyze if all F (liars) have equivalent neighbor configurations"""
    # Find any valid arrangement for n
    for arr in product([True, False], repeat=n):
        if not check_arrangement(arr) or not has_both_types(arr):
            continue
        
        # Analyze this arrangement
        f_neighbors = set()
        t_neighbors = set()
        
        for i in range(n):
            left = (i - 1) % n
            right = (i + 1) % n
            config = (arr[left], arr[right])
            if arr[i]:
                t_neighbors.add(config)
            else:
                f_neighbors.add(config)
        
        return len(f_neighbors) == 1, len(t_neighbors) == 1
    
    return None, None

def main():
    print("=" * 80)
    print("BANQUET LOGIC PUZZLE - FINAL SOLUTION")
    print("=" * 80)
    
    # Case 1: Lady=T, Gent=F -> 11 people
    print("\nCASE 1: Lady tells truth, Gent lies")
    print("  Implies: 11 people (Lady's claim is true)")
    scenarios_11 = find_valid_scenarios(11, True, False)
    print(f"  Valid scenarios: {len(scenarios_11)}")
    if scenarios_11:
        print(f"  Example pattern: {''.join(['T' if x else 'F' for x in scenarios_11[0][0]])}")
    
    # Case 2: Lady=F, Gent=T -> 10 people
    print("\nCASE 2: Lady lies, Gent tells truth")
    print("  Implies: 10 people (Gent's claim is true)")
    scenarios_10 = find_valid_scenarios(10, False, True)
    print(f"  Valid scenarios: {len(scenarios_10)}")
    if scenarios_10:
        print(f"  Example pattern: {''.join(['T' if x else 'F' for x in scenarios_10[0][0]])}")
    
    # Logical uniformity analysis
    print("\n" + "=" * 80)
    print("LOGICAL UNIFORMITY TEST")
    print("=" * 80)
    
    f_uniform_11, t_uniform_11 = analyze_neighbor_uniformity(11)
    f_uniform_10, t_uniform_10 = analyze_neighbor_uniformity(10)
    
    print(f"\n11 people: F uniform={f_uniform_11}, T uniform={t_uniform_11}")
    print(f"10 people: F uniform={f_uniform_10}, T uniform={t_uniform_10}")
    
    # Final conclusion
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if f_uniform_10 and t_uniform_10 and (not f_uniform_11 or not t_uniform_11):
        print("""
10-PERSON CASE:
  - All liars (F) have identical T-T neighbors [UNIFORM]
  - All truth-tellers (T) have identical F-F neighbors [UNIFORM]
  
11-PERSON CASE:
  - Liars (F) have MIXED neighbor configurations [NON-UNIFORM]
  - Some F have T-T neighbors, others have T-F or F-T neighbors
  
CRITICAL INSIGHT:
Anonymous participants of the same type must be logically equivalent.
The 11-person case violates this requirement.

*** ANSWER: 10 PEOPLE ***
""")
    else:
        print("Unable to determine unique answer")

if __name__ == "__main__":
    main()
