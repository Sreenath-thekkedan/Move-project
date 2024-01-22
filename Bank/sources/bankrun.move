// Module 0x1::Aptos
module 0x1::Aptos {
    use aptos_framework::timestamp;
    // Constants
    const MAX_SUPPLY: u64 = 1000000000; // Maximum token supply

    // Struct for  the token
    struct Token has key, copy, drop{
        value: u64,
    }

    // Function to mint new tokens and assign them to an account
    public fun mint(receiver: address, amount: u64) acquires Token {
        let new_balance = get_account_balance(receiver);
        assert!(new_balance <= MAX_SUPPLY, 2);
        save_balance(receiver, new_balance);
    }

    // Function to burn tokens
    public fun burn(owner: address, amount: u64) acquires Token {
        let current_balance = get_account_balance(owner);
        assert!(amount <= current_balance, 3);
        save_balance(owner, current_balance);
    }

    // Function to get the current balance 
    public fun get_account_balance(account: address): u64 acquires Token {
         let token_ref: &Token = borrow_global<Token>(account);
         token_ref.value
    }

    // Function to save the balance 
    public fun save_balance(account: address, balance: u64)  {
    }

    // Function to check if a subtraction operation would result in underflow
    public fun saturating_sub(a: u64, b: u64): u64 {
        if (a > b) {
            a - b
        } else {
            0
        }
    }
    // // Function to check if an additiion operation would result in overflow
    public fun saturating_add(a: u64, b: u64): u64 {
     let result = a + b;
     if (result >= a && result >= b) {
        result
      } else {
        MAX_SUPPLY
       }
    }
}
module 0x1::Bank {

    use aptos_framework::timestamp;

    //use 0x1::Aptos;
    //use 0x1::Time;
    // Constants
    const INIT_CORPUS: u64 = 10000; // Initial corpus amount
    const MIN_DURATION: u64 = 518400; // Minimum loan duration 1 year in minutes
    const MAX_DURATION: u64 = 5184000; // Maximum loan duration 10 years in minutes
    const PENALTY_RATE: u64 = 5; // Penalty rate for late payments (5%)
    const PREPAYMENT_FEE_RATE: u64 = 2; // Pre-payment fee rate (2%)

    // Struct to represent a loan
    struct Loan has copy, key, drop {
        borrower: address,
        principal: u64,
        interest_rate: u64,
        duration: u64,
        remaining_principal: u64,
        installment_amount: u64,
        last_payment_timestamp: u64,
    }

    // Function to calculate interest rate based on loan duration
    public fun calculateInterestRate(duration: u64): u64 {
        // Ensure the duration is within the allowed range
        assert!(duration >= MIN_DURATION && duration <= MAX_DURATION, 0);

        // Calculate interest rate inversely proportional to duration
        let interest_rate = 10000/ duration; 

       interest_rate
    }

    // Function to apply for a bank loan
    public fun applyForLoan(borrower: address, duration: u64): Loan acquires 0x1::Bank::Loan {
        // Ensure the duration is within the allowed range
        assert!(duration >= MIN_DURATION && duration <= MAX_DURATION, 0);

        // Calculate interest rate based on the duration
        let interest_rate = calculateInterestRate(duration);

        // Calculate principal amount
        let principal = INIT_CORPUS / 2; 
        // Calculate installment amount
        let installment_amount = (principal * interest_rate) / 100;

        // Initialize the loan struct
        let loan = Loan {
            borrower: borrower,
            principal: principal,
            interest_rate: interest_rate,
            duration: duration,
            remaining_principal: principal,
            installment_amount: installment_amount,
            last_payment_timestamp: 0
        };

        // Mint the loan amount to the borrower
        0x1::Aptos::mint(borrower, principal);

        // Return the loan details
         loan
    }

    // Function to make a loan installment payment
    public fun makePayment(loan: &Loan, payment_amount: u64) acquires 0x1::Aptos, Loan {
        // Ensure the payment is not late
        let current_timestamp = timestamp::now_seconds();
        assert!(current_timestamp <= loan.last_payment_timestamp + 30 * 60, 2); // Assuming 30 minutes as a month

        // Check if the payment amount is greater than the installment amount
        if (payment_amount > loan.installment_amount) {
            // Calculate pre-payment fee as some percentage of the pre-payment amount
            let prepayment_fee = (payment_amount - loan.installment_amount) * PREPAYMENT_FEE_RATE / 100; 

            // Deduct the pre-payment fee
            0x1::Aptos::burn(loan.borrower, prepayment_fee);
        };

        // Deduct the payment amount from the remaining principal
       let current_loan: &mut Loan;
       current_loan = borrow_global_mut<Loan>(loan.borrower);
       current_loan.remaining_principal = 0x1::Aptos::saturating_sub(current_loan.remaining_principal,payment_amount);



        // Apply penalty if the payment is late
        if (current_timestamp > loan.last_payment_timestamp + 7 * 24 * 60 * 60) {
            // Late payment penalty
            let penalty = (loan.installment_amount * PENALTY_RATE) / 100;
            current_loan.remaining_principal = loan.remaining_principal;
        };

        // Update the last payment timestamp
        current_loan.last_payment_timestamp = current_timestamp;


       // Check if the loan is fully paid
        if (loan.remaining_principal == 0) {
            // Burn the remaining principal from the borrower's account
            0x1::Aptos::burn(loan.borrower, loan.principal);
        };

        // Burn the payment amount from the borrower's account
        0x1::Aptos::burn(loan.borrower, payment_amount);
    }
}





 