#include "util.hpp"

#include <adapters.hpp>

#include <iostream>
#include <unordered_set>


using namespace jmr;
using namespace jmr::io;
using namespace jmr::operations;
using namespace joint;


class SplitToWordsMapper
{
private:
    IClient_Ptr _client;

public:
    using JointInterfaces = TypeList<IMapper>;

    SplitToWordsMapper(IClient_Ref client)
        : _client(client)
    { }

    void Process(IRowReader_Ref input, IRowWriter_Ref output)
    {
        while (auto row = input->ReadRow())
        {
            auto path = row->GetStringField("path");
            auto content = row->GetStringField("content");

            for (const auto& word : SplitString(content, ' '))
            {
                auto outRow = _client->CreateRow();
                outRow->SetStringField("path", path);
                outRow->SetStringField("word", word);
                output->WriteRow(outRow);
            }
        }
    }
};


class BuildPathsListReducer
{
private:
    IClient_Ptr _client;

public:
    using JointInterfaces = TypeList<IReducer>;

    BuildPathsListReducer(IClient_Ref client)
        : _client(client)
    { }

    void Process(StringRef key, IRowReader_Ref input, IRowWriter_Ref output)
    {
        std::unordered_set<std::string> paths;

        while (auto row = input->ReadRow())
        {
            auto path = row->GetStringField("path");
            paths.insert(path.Storage());
        }

        std::string pathsStr;
        for (const auto& path : paths)
            pathsStr += path + " ";

        auto outRow = _client->CreateRow();
        outRow->SetStringField("_word", key);
        outRow->SetStringField("paths", String(pathsStr));
        output->WriteRow(outRow);
    }
};


int main(int argc, const char** argv)
{
    std::vector<std::pair<String, String>> documents = {
        {"/doc1", "this is the first document"},
        {"/doc2", "this is the second document"},
        {"/doc3", "what is this"},
    };

    std::string executablePath(argv[0]);
    std::string executableDir(executablePath.substr(0, executablePath.find_last_of("/\\")));

    joint::Context ctx;
    joint::Module m(executableDir + "/core/Core.jm");
    auto client = m.GetRootObject<IClient>("MakeClient");

    std::cout << client->GetVersionString() << std::endl;

    auto writer = client->CreateTable("/input_documents");
    for (const auto& doc_pair : documents)
    {
        auto row = client->CreateRow();
        row->SetStringField("path", doc_pair.first);
        row->SetStringField("content", doc_pair.second);
        writer->WriteRow(row);
    }

    auto operation = client->RunMapReduce(
        MapReduceOpConfig{"word", "/input_documents", "/output_index"},
        ctx.MakeComponent<IMapper, SplitToWordsMapper>(client),
        ctx.MakeComponent<IReducer, BuildPathsListReducer>(client)
    );

    operation->Join();

    auto reader = client->ReadTable("/output_index");
    while (auto row = reader->ReadRow())
        std::cout << row->SerializeToJson() << std::endl;

    return 0;
}
