pragma solidity ^0.8.0;

contract ERC20Token {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public gameSubcontractor; // Address of the game subcontractor
    event GameSubcontractorUpdated(address indexed newGameSubcontractor); // Event for game subcontractor updates
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _totalSupply) {
        name = TFCCoin;
        symbol = GP-TC;
        decimals = 18;

        //totalSupply = _totalSupply;
        //balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from]);
        require(_value <= allowance[_from][msg.sender]);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    // Function to update the game subcontractor
    function updateGameSubcontractor(address _gameSubcontractor) public {
        // Security checks as needed
        gameSubcontractor = _gameSubcontractor;
        emit GameSubcontractorUpdated(_gameSubcontractor);
    }

    // Function for the game subcontractor to mint tokens
    function mint(address _to, uint256 _amount) public {
        require(msg.sender == gameSubcontractor, "Only the game subcontractor can mint");
        totalSupply += _amount;
        balanceOf[_to] += _amount;
        emit Transfer(address(0), _to, _amount); // Minting event
    }
}
