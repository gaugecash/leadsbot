// Importar contratos relevantes de OpenZeppelin
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/crowdsale/Crowdsale.sol";

// Contrato de Crowdsale refundable
contract RefundableCrowdsale is Crowdsale {
    // Variable para la meta de financiamiento
    uint256 public fundingGoal;

    // Mapping para llevar un registro de los aportes de los inversores
    mapping(address => uint256) public contributions;

    // Evento que se emite cuando se reembolsa a un inversor
    event Refund(address investor, uint256 amount);

    constructor(
        uint256 _fundingGoal,
        uint256 _rate, 
        address payable _wallet, 
        IERC20 _token
    ) 
        Crowdsale(_rate, _wallet, _token) 
    {
        require(_fundingGoal > 0);
        fundingGoal = _fundingGoal;
    }

    function _preValidatePurchase(address _beneficiary, uint256 _weiAmount) internal {
        super._preValidatePurchase(_beneficiary, _weiAmount);
        contributions[_beneficiary] = contributions[_beneficiary].add(_weiAmount);
    }

    function finalize() public {
        require(!super.isFinalized());
        require(goalReached());

        super._finalize();
    }

    function goalReached() public view returns (bool) {
        return weiRaised() >= fundingGoal;
    }

    function claimRefund(address payable _investor) public {
        require(!goalReached() && super.isFinalized());
        uint256 refund = contributions[_investor];
        _investor.transfer(refund);
        contributions[_investor] = 0;
        emit Refund(_investor, refund);
    }
}
