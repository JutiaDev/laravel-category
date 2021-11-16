<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use JutiaDev\Category\Models\Categorizable;
use JutiaDev\Category\Models\Category;

class AddCategoriesForeignKeyToRelatedModels extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     * @throws Exception
     */
    public function up()
    {
        $categoryReflection = new Category();

        process_category_related_models(function ($modelClass) use ($categoryReflection) {
            if (is_model_using_either_category_trait($modelClass)) {
                $modelReflection = new $modelClass;
                $modelTableName = $modelReflection->getTable();

                if (is_model_using_category_trait($modelClass)) {
                    if (Schema::hasColumn($modelTableName, $categoryReflection->getForeignKey())) {
                        $this->refreshModelCategoryFK($categoryReflection, $modelReflection);
                    } else {
                        $this->addModelCategoryFK($categoryReflection, $modelReflection);
                    }
                } elseif (Schema::hasColumn($modelTableName, $categoryReflection->getForeignKey())) {
                    $this->migrateModelCategoryDataToCategorizableTable($categoryReflection, $modelReflection);
                    $this->deleteModelCategoryFK($categoryReflection);
                }
            }
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     * @throws Exception
     */
    public function down()
    {
        $categoryReflection = new Category();

        process_category_related_models(function ($associatedModelClass) use ($categoryReflection) {
            if (is_model_using_category_trait($associatedModelClass)) {
                $modelReflection = new $associatedModelClass;

                // TODO: check there is a foreign key point to the category table
                // to avoid having a column with the same name as $categoryReflection->getForeignKey()
                if (Schema::hasColumn($modelReflection->getTable(), $categoryReflection->getForeignKey())) {
                    $this->deleteModelCategoryFK($categoryReflection);
                }
            }
        });
    }

    private function addModelCategoryFK(Category $categoryReflection, Model $modelReflection)
    {
        Schema::table(
            $modelReflection->getTable(),
            function (Blueprint $table) use ($categoryReflection, $modelReflection) {
                $table->unsignedBigInteger($categoryReflection->getForeignKey())
                    ->nullable()
                    ->after($modelReflection->getKeyName());
                $this->setForeignKey($table, $modelReflection);
            }
        );
    }

    private function refreshModelCategoryFK(Category $categoryReflection, Model $modelReflection)
    {
        Schema::table(
            $modelReflection->getTable(),
            function (Blueprint $table) use ($modelReflection, $categoryReflection) {
                $table->dropForeign([$categoryReflection->getForeignKey()]);
                $this->setForeignKey($table, $modelReflection);
            }
        );
    }

    private function setForeignKey(Blueprint $table, Model $modelReflection)
    {
        $fkDefinition = $table->foreign('category_id')
            ->references('id')
            ->on('categories');

        if ($modelReflection->getCascadeDeleteValue()) {
            $fkDefinition->cascadeOnDelete();
        } else {
            $fkDefinition->nullOnDelete();
        }
    }

    private function deleteModelCategoryFK(Model $modelReflection)
    {
        Schema::table($modelReflection->getTable(), function (Blueprint $table) {
            $table->dropForeign(['category_id']);
            $table->dropColumn('category_id');
        });
    }

    private function migrateModelCategoryDataToCategorizableTable(Category $categoryReflection, Model $modelReflection)
    {
        $modelClass = get_class($modelReflection);
        if (is_model_using_categories_trait($modelClass)) {
            $modelsWithCategories = ($modelReflection->newQuery())
                ->whereNotNull($categoryReflection->getForeignKey())
                ->get([$categoryReflection->getForeignKey(), "{$modelReflection->getKeyName()} as categorizable_id"]);

            Categorizable::insert(
                array_map(function ($modelWithCategory) use ($modelClass) {
                    $modelWithCategory['categorizable_type'] = $modelClass;
                    $modelWithCategory['created_at'] = now();
                    $modelWithCategory['updated_at'] = now();

                    return $modelWithCategory;
                }, $modelsWithCategories->toArray())
            );
        }
    }
}
