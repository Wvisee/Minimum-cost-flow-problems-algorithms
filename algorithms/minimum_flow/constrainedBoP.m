function SoPstruct = constrainedBoP(A0,theta,absorbing,weights)
%
%   A0 is the square adjacency matrix containing affinities, for example:
%
%   A0  =   [  0   1   1   0   0   0   0
%              1   0   1   0   0   0   0
%              1   1   0   1   0   0   0
%              0   0   1   0   1   1   1
%              0   0   0   1   0   1   1
%              0   0   0   1   1   0   1
%              0   0   0   1   1   1   0 ];
%
%   Each node j is supposed to be reachable from each node i.
%
%   theta must lie between eps (= 0.00000001) and 20.0.
%
%   weights  node weights, by defaut uniform.
%
%   absorbing %% = false if "non-hitting paths are considered" (defaut).
%             %% = true if "hitting paths are considered".
%
%   Returns SoPstruct structure containing the surprisal, the
%   potential and the RSP distance matrices and kernels.
%
%   Note: This code considers zero-length paths included in the set of
%   paths.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[nr,nc]=size(A0);

eps   = 1000 * realmin;
myMax = realmax;
conv_val = 1e-6;

if (nr ~= nc)
    fprintf('Error: The cost matrix is not square !\n');
    return;
end;

if issparse(A0)
    A0 = full(A0);
end

if nargin<3
    absorbing = false;
    weights = ones(nr,1)/nr;
end

if nargin<4
    weights = ones(nr,1)/nr;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
e = ones(nr,1);
I = eye(nr);
H = I - e*e'/nr;

% Computation of the cost matrix C (inverse of affinities)
C  = A0;
C(A0 >= eps) = 1./(A0(A0 >= eps));
C(C < eps)   = myMax;
A0(A0 < eps) = 0;

% Computation of P, the reference transition probabilities matrix
% representing the natural random walk on the graph
P = A0;
s = sum(P,2);
P = P./(s*e');

% sigma_in as weight
s_in = weights;
s_out = weights;

% Construction of the diffents elements which depends on absorbing option
if absorbing
    % matrices W and Z, vectors divisor and out_val
    W = exp(-theta * C) .* P;
    Z = (I - W)\I;
    divisor = diag(Z);
    numerator = diag(Z);
    out_val = s_out;
end
if ~absorbing
    % construction of alpha and n_ref
    Q = I - P';
    pinv_Q = pinv(Q);
    q = (I - pinv_Q * Q);
    q = q(:,1);
    
    n_ref_0 = pinv_Q * (s_in - P' * s_out);
    gamma = max((s_out - n_ref_0) ./ q) + 1;
    n_ref = n_ref_0 + gamma * q;
    alpha = s_out ./ n_ref;
    P_mod = (I - diag(alpha)) * P;
    
    % matrices W and Z, vectors divisor and out_val
    W = exp(-theta * C) .* P_mod;
    Z = (I - W)\I;
    divisor = ones(nr,1);
    numerator = n_ref;
    out_val = alpha;
end

m_in = e;
m_out = e;
convergence = false;
iter = 0;
while ~convergence
    m_out_prev = m_out;
    m_in = e ./ (Z * (m_out .* out_val ./ divisor));
    m_out = numerator ./ (Z' * (m_in .* s_in));
    max_diff = max(abs(m_out_prev - m_out));
    if max_diff < conv_val || iter > 10000
        convergence = true;
    end
    iter = iter +1;
end
Pi_CBOP = diag(m_in .* s_in) * Z * diag(m_out .* out_val ./ divisor);


%D_CBOP = abs(log(diag(1 ./ diag(Pi_CBOP)) * Pi_CBOP));
%D_CBOP = (D_CBOP + D_CBOP')/2;
D_CBOP = -(log(Pi_CBOP) + log(Pi_CBOP'))/2;
D_CBOP = D_CBOP - diag(diag(D_CBOP));

D_CBOP(D_CBOP>myMax/(nr*(nr-1))) = myMax/(nr*(nr-1));
D_CBOP(isinf(D_CBOP)) = myMax/(nr*(nr-1));


% Gaussian kernel from the CBOP distance
a   = 1;
D2 = D_CBOP .* D_CBOP;
sig = sum(sum(D2))/(nr*(nr-1));
Krg = exp(-a* (D2)/sig); % Compute a gaussian kernel matrix from D
Krg =(Krg+Krg')/2;
Krg = real(Krg);
[U,Lam] = eig(Krg); % remove negative eigenvalues for semi-definiteness
if ( (sum(diag(Lam) >= 0)) ~= nr)
    Lam = max(real(Lam),0);
    U = real(U);
    Krg = U*Lam*U';
    Krg =(Krg+Krg')/2;
    Krg = real(Krg);
end

% MDS kernel from the CBOP distance
Ks  = -0.5 * H*(D_CBOP .* D_CBOP)*H; % Compute a MDS kernel matrix from D by multidimensional scaling
Ks =(Ks+Ks')/2;
Ks = real(Ks);
[U,Lam] = eig(Ks); % remove negative eigenvalues for semi-definiteness
if ( (sum(diag(Lam) >= 0)) ~= nr)
    Lam = max(real(Lam),0);
    U = real(U);
    Ks = U*Lam*U';
    Ks =(Ks+Ks')/2;
    Ks = real(Ks);
end




SoPstruct.Dcbop = D_CBOP;
SoPstruct.Krg  = Krg; % The gaussian kernel associated to the CBOP distance matrix
SoPstruct.Ks = Ks; % The MDS kernel associated to the CBOP distance matrix
end
