#include "crocoddyl/multibody/costs/control.hpp"

namespace crocoddyl {

CostModelControl::CostModelControl(pinocchio::Model* const model, ActivationModelAbstract* const activation,
                                   const Eigen::VectorXd& uref)
    : CostModelAbstract(model, activation, (const unsigned)uref.size()), uref_(uref) {
  assert(activation->get_nr() == (const unsigned)uref.size() &&
         "CostModelControl: activation::nr is not equals to nu");
}

CostModelControl::CostModelControl(pinocchio::Model* const model, ActivationModelAbstract* const activation)
    : CostModelAbstract(model, activation), uref_(Eigen::VectorXd::Zero(activation->get_nr())) {}

CostModelControl::CostModelControl(pinocchio::Model* const model, ActivationModelAbstract* const activation,
                                   const unsigned int& nu)
    : CostModelAbstract(model, activation, nu), uref_(Eigen::VectorXd::Zero(nu)) {
  assert(activation->get_nr() == nu_ && "CostModelControl: activation::nr is not equals to nu");
}

CostModelControl::CostModelControl(pinocchio::Model* const model, const Eigen::VectorXd& uref)
    : CostModelAbstract(model, (unsigned int)uref.size(), (unsigned int)uref.size()), uref_(uref) {}

CostModelControl::CostModelControl(pinocchio::Model* const model)
    : CostModelAbstract(model, model->nv), uref_(Eigen::VectorXd::Zero(model->nv)) {}

CostModelControl::CostModelControl(pinocchio::Model* const model, const unsigned int& nu)
    : CostModelAbstract(model, nu, nu), uref_(Eigen::VectorXd::Zero(nu)) {}

CostModelControl::~CostModelControl() {}

void CostModelControl::calc(boost::shared_ptr<CostDataAbstract>& data, const Eigen::Ref<const Eigen::VectorXd>&,
                            const Eigen::Ref<const Eigen::VectorXd>& u) {
  data->r = u - uref_;
  activation_->calc(data->activation, data->r);
  data->cost = data->activation->a_value;
}

void CostModelControl::calcDiff(boost::shared_ptr<CostDataAbstract>& data, const Eigen::Ref<const Eigen::VectorXd>& x,
                                const Eigen::Ref<const Eigen::VectorXd>& u, const bool& recalc) {
  if (recalc) {
    calc(data, x, u);
  }
  activation_->calcDiff(data->activation, data->r, recalc);
  data->Lu = data->activation->Ar;
  data->Luu.diagonal() = data->activation->Arr.diagonal();
}

const Eigen::VectorXd& CostModelControl::get_uref() const { return uref_; }

}  // namespace crocoddyl