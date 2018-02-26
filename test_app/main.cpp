#include <adapters.hpp>

#include <iostream>

using namespace jmr;
using namespace joint;

class MyMapper
{
public:
    using JointInterfaces = TypeList<IMapper>;

    void Process(IRowReader_Ref input, IRowWriter_Ref output)
    {
        while (auto row = input->ReadRow())
        {
            row->SetI32Field("num", row->GetI32Field("num") * 10);
            output->WriteRow(row);
        }
    }
};

int main(int argc, const char** argv)
{
    std::string executablePath(argv[0]);
    std::string executableDir(executablePath.substr(0, executablePath.find_last_of("/\\")));

    joint::Context ctx;
    joint::Module m(executableDir + "/core/Core.jm");
    auto clientSession = m.GetRootObject<IClientSession>("MakeClientSession");

    std::cout << clientSession->GetVersionString() << std::endl;

    auto writer = clientSession->CreateTable("/input_table");
    for (int i = 0; i < 10; ++i)
    {
        auto row = clientSession->CreateRow();
        row->SetI32Field("num", i);
        writer->WriteRow(row);
    }

    auto operation = clientSession->RunMap(
        MapOpConfig{"/input_table", "/output_table"},
        ctx.MakeComponent<IMapper, MyMapper>()
    );

    operation->Join();

    auto reader = clientSession->ReadTable("/output_table");
    while (auto row = reader->ReadRow())
        std::cout << "num: " << row->GetI32Field("num") << std::endl;

    return 0;
}
